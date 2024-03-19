
from django.db import *
from django.db.models import *
from django_mailbox.models import Message, Mailbox, MessageAttachment



def process_mail():

    m_messages = Message.objects.filter(Q(from_header__contains='<')|Q(to_header__contains='<'))

    for m_message in m_messages:
        m_message.from_header = m_message.from_address
        m_message.to_header = m_message.to_address
        m_message.save()
