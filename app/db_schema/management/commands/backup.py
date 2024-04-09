from django.core.management.base import BaseCommand, CommandError
from django.core import management
from django.db import transaction
from django.db.models import *


class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options):

        from datetime import datetime
        
        today = datetime.now().strftime("YYYY-MM-DD")
        management.call_command(f"dbbackup -o cms_wavemaster_db_backup_{today}.sql")
        management.call_command(f"mediabackup -o cms_wavemaster_media_backup_{today}.tar")
