from rest_framework import serializers

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

    class Meta:
        model = Customer
        fields = "__all__"


class CustomerMemoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerMemo
        fields = ["id", "memo", "memo_date"]


class MailTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MailTemplate
        fields = ["id", "subject", "body"]


class AttachmentFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttachmentFile
        fields = ['id', 'file', "is_used"]


class MailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    manager = UserSerializer(read_only=True)
    attachments = AttachmentFileSerializer(read_only=True)
    class Meta:
        model = Mail
        fields = "__all__"