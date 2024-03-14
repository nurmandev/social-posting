from rest_framework import serializers
import json

from db_schema.models import *
from django_mailbox.models import Message, MessageAttachment


class MessageAttachmentSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField()

    class Meta:
        model = MessageAttachment
        fields = ["id", "document"]

    def get_document(self, obj):
        
        return {
            "name": obj.document.file.name,
            "url": obj.document.file.url,
            "content_type": obj.document.file.content_type
        }


class MessageSerializer(serializers.ModelSerializer):
    attachments = MessageAttachmentSerializer(many=True)
    body = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_body(self, obj):

        return obj.html