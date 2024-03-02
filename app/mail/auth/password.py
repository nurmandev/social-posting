
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions import *
from django.db.models import *
from django.db import transaction
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from db_schema.models import *
from db_schema.serializers import *
import datetime

def send_mail(request, email, token):
    m_user = User.objects.get(email=email)
    
    reset_password_url = f"http://localhost:3000/accounts/password/reset?token={token}"
    expire_at =  (datetime.datetime.now()+ datetime.timedelta(days=3)).strftime("%Y/%m/%d %H:%M")
    
    # Send the password reset email
    mail_subject = "パスワードを設定・変更してください"
    message = render_to_string("mail_template/password_forgot.html", {
        "name": f"{m_user.user_info.name}",
        "url": reset_password_url,
        "expire_at": expire_at,
    })

    message = message
    email_obj = EmailMessage(
        mail_subject, message, to=[m_user.email]
    )
    email_obj.content_subtype = "html"
    email_obj.send()
