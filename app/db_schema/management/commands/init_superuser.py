from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password

from db_schema.models import *
import json



class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options):
        try:
            user_info = UserInfo.objects.create(name='Akira', last_name='Murayama', first_name='Akira', name_furi='ムラヤマ', last_name_furi='ムラヤマ', first_name_furi='アキラ', phone='080-1234-5678')
            m_user = User.objects.create(user_info=user_info, email='akira.murayama.dev@gmail.com', password=make_password('password'), permission='super', is_active=True, is_superuser=True, is_staff=True)
        except Exception as e:
            print(str(e))
            raise CommandError('Failed to create super user')
