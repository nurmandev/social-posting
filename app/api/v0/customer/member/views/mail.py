

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from utils.permissions import *
from django.db.models import *
from django.db import transaction

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django_mailbox.models import Message, Mailbox, MessageAttachment

from db_schema.models import *
from db_schema.serializers import *

from ..tasks import send_email_task
from validations.mail import validate_create_mail


class CreateMailAPI(APIView):
    permission_classes = [IsCustomer]


    def post(self, request):
        try:
            errors, status, clean_data = validate_create_mail(request)

            if status != 200:
                return Response({"errors": errors}, status=status)

            for recepient in clean_data['recepients']:
                send_email_task.delay(recepient, clean_data['subject'], clean_data['body'], clean_data['attachment'])

            return Response({
                "msg": ""
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
