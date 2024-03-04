from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.db.models import *
from django.db import transaction

from db_schema.models import *
from db_schema.serializers import *
from utils.permissions import *

# Create your views here.

class GetRoleAPI(APIView):
    parser_classes = [MultiPartParser]
    
    def get(self, request):
    
        try:
            m_data = Role.objects.all()
            serializer = RoleSerializer(m_data, many=True)

            return Response(serializer.data, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": "Internal Server Error"}, status=500)



class GetStatusAPI(APIView):
    parser_classes = [MultiPartParser]
    
    def get(self, request):
    
        try:
            m_data = Status.objects.all()
            serializer = StatusSerializer(m_data, many=True)

            return Response(serializer.data, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": "Internal Server Error"}, status=500)



class GetPropertyAPI(APIView):
    parser_classes = [MultiPartParser]
    
    def get(self, request):
    
        try:
            m_data = Property.objects.all()
            serializer = PropertySerializer(m_data, many=True)

            return Response(serializer.data, status=200)
        except Exception as e:
            print(str(e))
            return Response({"msg": "Internal Server Error"}, status=500)

