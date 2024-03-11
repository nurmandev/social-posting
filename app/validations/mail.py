
from django.db.models import *
from db_schema.models import *
import re


def validate_create_mail(request):
    data = dict(request.data)
    recepients = data.get("recepients", [])
    subject = data.get("subject", "")
    body = data.get("body", "")
    attachment = data.get("attachment", [])
    

    try:
        errors = {}

        if len(recepients) == 0:
            errors["recepients"] = "受信者を入力してください"

        if subject == "":
            errors["subject"] = "件名を入力してください"

        if body == "":
            errors["body"] = "本文を入力してください"

        status = 422 if len(errors) > 0 else 200
        clean_data = {
            "recepients": recepients,
            "subject": subject,
            "body": body,
            "attachment": attachment
        }

        return errors, status, clean_data
        
    except Exception as e:
        print(str(e))
        
        return {}, 500, {}
    