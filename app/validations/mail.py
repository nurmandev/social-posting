
from django.db.models import *
from db_schema.models import *
import re


def validate_create_mail(request):
    data = dict(request.data)
    recipients = data.get("recipients", [])
    subject = data.get("subject", "")
    body = data.get("body", "")
    attachment = data.get("attachment", [])
    

    try:
        errors = {}

        if len(recipients) == 0:
            errors["recipients"] = "受信者を入力してください"

        if subject == "":
            errors["subject"] = "件名を入力してください"

        if body == "":
            errors["body"] = "本文を入力してください"

        status = 422 if len(errors) > 0 else 200
        clean_data = {
            "recipients": recipients,
            "subject": subject,
            "body": body,
            "attachment": attachment
        }

        return errors, status, clean_data
        
    except Exception as e:
        print(str(e))
        
        return {}, 500, {}
    