from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from django.http import FileResponse
from django.conf import settings

from utils.permissions import *
from django.db.models import *
from db_schema.models import *
from db_schema.serializers import *



class GetBackupListAPI(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        keyword = request.GET.get('keyword', '')
        page = int(request.GET.get('page', 1))
        pageSize = int(request.GET.get('pageSize', 10))
        
        try:
            # get file list from backup dir
            import os
            import datetime

            backup_dir = os.path.join(settings.BASE_DIR, 'backup')
            backup_files = os.listdir(backup_dir)

            result = []

            for backup_file in backup_files:
                if backup_file.startswith('cms_wavemaster_db_backup_') and backup_file.endswith('.sql') and keyword in backup_file:
                    time = backup_file.replace('cms_wavemaster_db_backup_', '').replace('.sql', '')
                    
                    if f"cms_wavemaster_media_backup_{time}.tar" in backup_files:
                        result.append({
                            'time': time,
                            'db': backup_file,
                            'media': f"cms_wavemaster_media_backup_{time}.tar"
                        })
            
            return Response({
                "data": result[pageSize * (page - 1):pageSize * page],
                "total": len(result)
            })
        
        except Exception as e:
            print(str(e))
            return Response({
                "data": [],
                "total": 0
            })
        

class BackupAPI(APIView):
    permission_classes = [IsOwner]

    def post(self, request):
        data = dict(request.data)
        time = data.get('time', '')

        try:
            from django.core import management
            from datetime import datetime
            import os

            base_dir = os.path.join(settings.BASE_DIR, 'backup')
            if not os.path.exists(os.path.join(base_dir, f"cms_wavemaster_db_backup_{time}.sql")) or not os.path.exists(os.path.join(base_dir, f"cms_wavemaster_media_backup_{time}.tar")):
                raise Exception("バックアップファイルが見つかりません")
            
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
            management.call_command(f"dbbackup", f"-otemp_cms_wavemaster_db_backup_{today}.sql")
            management.call_command(f"mediabackup", f"-otemp_cms_wavemaster_media_backup_{today}.tar")


            management.call_command(f"dbrestore", f"-i{os.path.join(base_dir, f'cms_wavemaster_db_backup_{time}.sql')} --noinput")
            management.call_command(f"mediarestore", f"-i{os.path.join(base_dir, f'cms_wavemaster_media_backup_{time}.tar')} --noinput")

            return Response("バックアップが完了しました")
        except Exception as e:
            print(str(e))
            return Response("バックアップに失敗しました", status=500)


class DownloadBackupAPI(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        time = request.GET.get('time', '')
        backup_type = request.GET.get('type', '')

        if backup_type not in ['db', 'media']:
            raise Exception("Invalid backup type")

        if backup_type == 'db':
            backup_file = f"cms_wavemaster_db_backup_{time}.sql"
        else:
            backup_file = f"cms_wavemaster_media_backup_{time}.tar"

        try:
            import os

            with open(os.path.join(settings.BASE_DIR, 'backup', backup_file), 'rb') as f:
                response = FileResponse(f)
                response['Content-Disposition'] = f'attachment; filename="{backup_file}"'
                return response
        except Exception as e:
            print(str(e))
            return Response("バックアップファイルが見つかりません", status=404)