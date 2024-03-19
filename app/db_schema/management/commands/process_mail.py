from django.core.management.base import BaseCommand, CommandError
from django.db import *
from django.db.models import *
from django_mailbox.models import Message, Mailbox, MessageAttachment
from db_schema.models import *
import json



class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options):
        
        m_messages = Message.objects.filter(Q(from_header__contains='<')|Q(to_header__contains='<'))

        for m_message in m_messages:
            pass
            # m_message.from_header = m_message.from_address
            # m_message.to_header = m_message.to_addresses
            # m_message.save()
