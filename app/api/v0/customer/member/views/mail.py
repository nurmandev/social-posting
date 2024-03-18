

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from utils.permissions import *
from django.db.models import *
from django.db import transaction

from django_mailbox.models import Message, Mailbox, MessageAttachment
from ..serializers import *
from db_schema.models import *
from db_schema.serializers import *

from ..tasks import send_email_task
from validations.mail import *


class GetMailsAPI(APIView):
    permission_classes = [IsCustomerAndMember|IsCustomerAndAdmin]

    def get(self, request):
        try:
            mails = Message.objects.filter()
            serializer = MessageSerializer(mails, many=True)
            return Response({
                "mails": serializer.data
            }, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)

class CreateMailAPI(APIView):
    permission_classes = [IsCustomer]


    def post(self, request):
        try:
            errors, status, clean_data = validate_create_mail(request)

            if status != 200:
                return Response({"errors": errors}, status=status)

            for recipient in clean_data['recipients']:
                send_email_task.delay(recipient, clean_data['subject'], clean_data['body'], clean_data['attachment'])

            return Response({
                "msg": "メールを送信しました。"
            }, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)
        

class CreateGroupMailAPI(APIView):
    permission_classes = [IsCustomer]


    def post(self, request):
        try:
            errors, status, clean_data = validate_create_group_mail(request)

            if status != 200:
                return Response({"errors": errors}, status=status)

            if clean_data['group_type'] == "status":
                recipients = Customer.objects.filter(status=Status.objects.get(id=clean_data['group']))
                
            if clean_data['group_type'] == "property":
                recipients = Customer.objects.filter(property=Property.objects.get(id=clean_data['group']))
                
            for recipient in recipients:
                send_email_task.delay(recipient.id, clean_data['subject'], clean_data['body'], clean_data['attachment'])

            return Response({
                "msg": "メールを送信しました。"
            }, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)
        

        
class CreateAttachmentFileView(APIView):
    # permission_classes = [IsCustomerAndMember|IsCustomerAndAdmin]
    parser_classes = [MultiPartParser]
    
    def post(self, request):
    
        try:
            if request.data.get('file') is None:
                return Response({"msg": "File is required"}, status=400)
            
            m_attach = MessageAttachment.objects.create(
                document=request.data.get('file')
            )
        
            return Response({
                "success": True,
                "id": m_attach.id
            }, status=200)
        
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)
