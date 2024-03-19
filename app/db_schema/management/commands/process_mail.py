from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import *
from django_mailbox.models import Message, Mailbox, MessageAttachment
from db_schema.models import *
import json



class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options):
        
        m_box = Mailbox.objects.all().first()
        
        if m_box:
            m_messages = m_box.get_new_mail()

            for message in m_messages:
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
                    continue

                with transaction.atomic():
                    
                    m_mail = Mail.objects.create(
                        outgoing=False,
                        read=None,
                        subject=message.subject,
                        body=message.text if message.html is None else message.html,
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

                    print(m_mail)