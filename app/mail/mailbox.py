
from utils.permissions import *
from django.db.models import *
from django.db import transaction
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django_mailbox.models import Message, Mailbox, MessageAttachment
from config.celery import app

from db_schema.models import *
from db_schema.serializers import *

# @app.task
def send_email_task(recepients, subject, body, attachment):
    recepient_users = Customer.objects.filter(id__in=recepients)
    
    mail_subject = subject

    email_obj = EmailMessage(
        mail_subject, body, to=[recepient_user.email for recepient_user in recepient_users]
    )
    email_obj.content_subtype = "html"

    for attach_id in attachment:
        m_attach = MessageAttachment.objects.get(id = attach_id)
        email_obj.attach(m_attach.document.file.name, m_attach.document.file.read(), m_attach.document.file.content_type)

    email_obj.send()

    m_box = Mailbox.objects.all().first()

    # save email_obj to Message
    m_box.record_outgoing_message(email_obj.message())