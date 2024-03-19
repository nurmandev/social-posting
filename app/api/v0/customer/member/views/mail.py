

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
from datetime import datetime
from ..tasks import send_email_task
from validations.mail import *


class GetInboxMailsAPI(APIView):
    permission_classes = [IsCustomerAndMember|IsCustomerAndAdmin]

    def get(self, request):
        try:
            page = int(request.GET.get('page', 1))
            pageSize = int(request.GET.get('pageSize', 20))

            # get incoming mails according to customers
            m_customer_ids = Mail.objects.filter(outgoing=False).values_list('customers', flat=True)

            m_customers = Customer.objects.filter(id__in=m_customer_ids).order_by('-last_contacted')
            
            serializer = MailInboxSerializer(m_customers[(page-1)*pageSize : page*pageSize] , many=True)

            return Response({
                "data": serializer.data,
                "total": m_customers.count(),
                "message_unread": Mail.objects.filter(outgoing=False, read=None, managers=request.user).count(),
                "message_total": Mail.objects.filter(managers=request.user).count()
            }, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)


class GetSentMailsAPI(APIView):
    permission_classes = [IsCustomerAndMember|IsCustomerAndAdmin]

    def get(self, request):
        try:
            page = int(request.GET.get('page', 1))
            pageSize = int(request.GET.get('pageSize', 20))

            # get incoming mails according to customers
            m_mails = Mail.objects.filter(outgoing=True)

            serializer = MailSerializer(m_mails[(page-1)*pageSize : page*pageSize] , many=True)

            return Response({
                "data": serializer.data,
                "total": m_mails.count()
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

            recipients = Customer.objects.filter(id__in=clean_data['recipients'])
            send_email_task([r.id for r in recipients], clean_data['subject'], clean_data['body'], clean_data['attachment'])

            # recipients = Customer.objects.filter(id__in=clean_data['recipients'])
            # recipients = list(recipients)
            # recipients = [recipients[i:i + 1000] for i in range(0, len(recipients), 1000)]
                
            # for sub_recipients in recipients:
            #     send_email_task.delay([r.id for r in sub_recipients], clean_data['subject'], clean_data['body'], clean_data['attachment'])
            
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
                
                
            send_email_task([r.id for r in recipients], clean_data['subject'], clean_data['body'], clean_data['attachment'])
            
            # chunk the recipients into 1000 sublists
            # recipients = list(recipients)
            # recipients = [recipients[i:i + 1000] for i in range(0, len(recipients), 1000)]
                
            # for sub_recipients in recipients:
            #     send_email_task.delay([r.id for r in sub_recipients], clean_data['subject'], clean_data['body'], clean_data['attachment'])

            return Response({
                "msg": "メールを送信しました。"
            }, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)
        

class GetMailsByCustomer(APIView):
    permission_classes = [IsCustomerAndMember|IsCustomerAndAdmin]

    def get(self, request, customer_id):
        try:
            m_customer = Customer.objects.get(id=customer_id, manager=request.user)
            
            if m_customer is None:
                raise Exception("Customer not found")
            
            m_mails = Mail.objects.filter(customers=m_customer).order_by('processed')
            serializer = MailSerializer(m_mails, many=True)

            for mail in m_mails:
                for attach in mail.attachments.all():
                    print(attach.document.url)

            return Response({
                "data": serializer.data,
                "total": m_mails.count(),
                "customer": CustomerSerializer(m_customer).data
            }, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": str(e)}, status=500)

        
class MakeMailAsRead(APIView):
    permission_classes = [IsCustomer]

    def post(self, request, mail_id):
        try:
            m_mail = Mail.objects.filter(id=mail_id, managers=request.user).first()
            if m_mail is None:
                raise Exception("Mail not found")

            with transaction.atomic():
                if m_mail.read is None:
                    m_mail.read = datetime.now()
                    m_mail.save()
                    
            return Response({}, status=200)
        
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
