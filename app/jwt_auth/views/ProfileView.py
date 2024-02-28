from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password, make_password
from utils.permissions import IsAuthenticated
from django.db.models import *
from django.db import transaction

from db_schema.models import *
from db_schema.serializers import *

# Create your views here.
class GetMyAccountInfoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user).data
        return Response({"me": serializer})
    
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        try:
            data = UserInfoSerializer(request.user.user_info).data
            data["email"] = request.user.email
            data['permission'] = request.user.permission
            return Response(data, 200)

        except Exception as e:
            print(str(e))
            return Response({"msg": "Can't find User Info"}, status=404)
    
    def post(self, request):
        data = dict(request.data)
        
        try:
            pass
        except Exception as e:
            print(str(e))
            return Response({"msg": "Internal Server Error"}, status=400)