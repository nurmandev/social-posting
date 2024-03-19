from rest_framework import serializers
from django_mailbox.models import Message, Mailbox, MessageAttachment
from django.db.models import *

from .models import *
from jwt_auth.serializers import *

class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ['id', 'name']


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ['id', 'name']


class CustomerSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    manager = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"

class CustomerNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ["id", "name", "email"]

class CustomerFlatSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        exclude = ["created_at", "updated_at"]


class CustomerMemoSerializer(serializers.ModelSerializer):
    manager = UserSerializer(read_only=True)

    class Meta:
        model = CustomerMemo
        fields = ["id", "content", "manager", "customer", "created_at"]


class MailTemplateSerializer(serializers.ModelSerializer):
    publisher = UserSerializer(read_only=True)
    class Meta:
        model = MailTemplate
        fields = ["id", "subject", "body", "publisher"]

class MessageAttachmentSerializer(serializers.ModelSerializer):


    class Meta:
        model = MessageAttachment
        fields = "__all__"


class MailSerializer(serializers.ModelSerializer):
    customers = CustomerNameSerializer(many=True)
    managers = UserNameSerializer(many=True)
    attachments = MessageAttachmentSerializer(many=True)

    class Meta:
        model = Mail
        fields = "__all__"

