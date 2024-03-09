from django_mailbox.signals import message_received
from django.dispatch import receiver

@receiver(message_received)
def dance_jig(sender, message, **args):
    print(sender)
    print(message)