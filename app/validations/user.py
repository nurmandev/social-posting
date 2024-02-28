
from django.db.models import *
from db_schema.models import *
import re


def validate_create_user(request):
    data = dict(request.data)
    email = data.get("email", "")
    password = data.get("password", "")
    last_name = data.get("last_name", "")
    first_name = data.get("first_name", "")
    phone = data.get("phone", "")
    role = data.get("role", "")

    try:
        errors = {}

        if email == "":
            errors["email"] = "メールを入力してください。"

        if email != "" and User.objects.filter(email=email).exists():
            errors["email"] = "このメールは既に登録されています。"

        if password == "":
            errors["password"] = "パスワードを入力してください。"

        if last_name == "":
            errors["last_name"] = "姓を入力してください。"

        if first_name == "":
            errors["first_name"] = "名を入力してください。"

        if Role.objects.filter(role_id=role).exists() == False:
            errors["role"] = "この権限は存在しません。"


        status = 422 if len(errors) > 0 else 200
        clean_data = {
            "email": email,
            "password": password,
            "last_name": last_name,
            "first_name": first_name,
            "phone": phone,
            "role": role
        }

        return errors, status, clean_data
        
    except Exception as e:
        print(str(e))
        
        return {}, 500, {}
    
def validate_update_user(request, user_id):
    data = dict(request.data)
    email = data.get("email", "")
    password = data.get("password", "")
    last_name = data.get("last_name", "")
    first_name = data.get("first_name", "")
    phone = data.get("phone", "")
    role = data.get("role", "")

    try:
        errors = {}

        if email == "":
            errors["email"] = "メールを入力してください。"

        if email != "" and User.objects.filter(Q(email=email), ~Q(id=user_id)).exists():
            errors["email"] = "このメールは既に登録されています。"

        if password == "":
            errors["password"] = "パスワードを入力してください。"

        if last_name == "":
            errors["last_name"] = "姓を入力してください。"

        if first_name == "":
            errors["first_name"] = "名を入力してください。"

        if Role.objects.filter(role_id=role).exists() == False:
            errors["role"] = "この権限は存在しません。"


        status = 422 if len(errors) > 0 else 200
        clean_data = {
            "email": email,
            "password": password,
            "last_name": last_name,
            "first_name": first_name,
            "phone": phone,
            "role": role
        }

        return errors, status, clean_data
        
    except Exception as e:
        print(str(e))
        
        return {}, 500, {}
    