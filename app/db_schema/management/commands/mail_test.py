from django.core.management.base import BaseCommand, CommandError
from django.db import *
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django_mailbox.models import Message, Mailbox, MessageAttachment
from celery import shared_task
from config.celery import app
from django.db.models import *
from django_mailbox.models import Message, Mailbox, MessageAttachment
from db_schema.models import *
import json



class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options):
        subject = "Test"
        body = "Test"
        attachment = []
        recepient = 1
        recepient_user = Customer.objects.get(id=recepient)

        mail_subject = subject

        email_obj = EmailMessage(
            mail_subject, body, to=[recepient_user.email]
        )
        email_obj.content_subtype = "html"

        for attach_id in attachment:
            m_attach = MessageAttachment.objects.get(id = attach_id)
            email_obj.attach(m_attach.document.file.name, m_attach.document.file.read(), m_attach.document.file.content_type)

        email_obj.send()

        m_box = Mailbox.objects.all().first()

        # save email_obj to Message
        m_box.record_outgoing_message(email_obj.message())