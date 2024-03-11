from rest_framework import serializers
import json

from db_schema.models import *
from django_mailbox.models import Message, MessageAttachment


class MessageAttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageAttachment
        fields = ["id", "document"]


class MessageSerializer(serializers.ModelSerializer):
    attachments = MessageAttachmentSerializer(many=True)
    body = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_body(self, obj):

        return obj.get_body()