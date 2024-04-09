from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import *

class Command(BaseCommand):
    help = "Closes the specified poll for voting"


    def handle(self, *args, **options):
        
        # get file list from backup dir
        import os
        import datetime

        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        backup_dir = os.path.join(settings.BASE_DIR, 'backup')
        backup_files = os.listdir(backup_dir)

        result = []

        for backup_file in backup_files:
            if backup_file.startswith('cms_wavemaster_db_backup_') and backup_file.endswith('.sql'):
                time = backup_file.replace('cms_wavemaster_db_backup_', '').replace('.sql', '')
                
                if f"cms_wavemaster_media_backup_{time}.tar" in backup_files:
                    result.append({
                        'time': time,
                        'db': backup_file,
                        'media': f"cms_wavemaster_media_backup_{time}.tar"
                    })
        
        print(result)