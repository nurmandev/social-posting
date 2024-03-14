
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions import *
from django.db.models import *
from django.db import transaction
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django_mailbox.models import Message, Mailbox, MessageAttachment
from celery import shared_task

from db_schema.models import *
from db_schema.serializers import *
import datetime

@shared_task
def send_email_task(recipient, subject, body, attachment):
    recipient_user = Customer.objects.get(id=recipient)
    
    mail_subject = subject

    email_obj = EmailMessage(
        mail_subject, body, to=[recipient_user.email]
    )
    email_obj.content_subtype = "html"

    for attach_id in attachment:
        m_attach = MessageAttachment.objects.get(id = attach_id)
        email_obj.attach(m_attach.document.file.name, m_attach.document.file.read(), m_attach.document.file.content_type)

    email_obj.send()

    m_box = Mailbox.objects.all().first()

    # save email_obj to Message
    mail = Message(mailbox=m_box, subject=mail_subject, message_id=email_obj.message().get("Message-ID"), from_header=f"{recipient_user.manager.user_info.name} <{email_obj.from_email}>", to_header=f"{recipient_user.name} <{recipient_user.email}>", outgoing=True)
    mail.set_body(body)
    mail.save()    
