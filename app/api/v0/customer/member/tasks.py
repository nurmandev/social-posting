
from utils.permissions import *
from django.db.models import *
from django.db import transaction
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django_mailbox.models import Message, Mailbox, MessageAttachment

from db_schema.models import *
from db_schema.serializers import *
from datetime import datetime

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
    message = m_box.record_outgoing_message(email_obj.message())

    if message.outgoing:
        m_customers = Customer.objects.filter(Q(email__in=message.to_addresses) | Q(email_2__in=message.to_addresses))
    else:
        m_customers = Customer.objects.filter(Q(email__in=message.from_address) | Q(email_2__in=message.from_address))
    
    if message.outgoing:
        m_managers = Customer.objects.filter(Q(email__in=message.to_addresses) | Q(email_2__in=message.to_addresses)).values_list('manager', flat=True)
        m_managers = User.objects.filter(id__in=m_managers)
    else:
        m_managers = Customer.objects.filter(Q(email__in=message.from_address) | Q(email_2__in=message.from_address)).values_list('manager', flat=True)
        m_managers = User.objects.filter(id__in=m_managers)

    if m_customers.count() == 0 or m_managers.count() == 0:
        return

    with transaction.atomic():
        m_mail = Mail.objects.create(
            outgoing=True,
            read=datetime.now(),
            subject=message.subject,
            body=message.text,
            processed=message.processed
        )

        m_attachments = MessageAttachment.objects.filter(message=message)
        for attach  in m_attachments:
            m_mail.attachments.add(attach)

        for customer in m_customers:
            customer.last_contacted = message.processed
            customer.save()
            m_mail.customers.add(customer)

        for manager in m_managers:
            m_mail.managers.add(manager)
