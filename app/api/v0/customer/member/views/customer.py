from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import *
from django.db import transaction
from django.contrib.auth.hashers import check_password, make_password

from db_schema.models import *
from db_schema.serializers import *
from utils.permissions import *
from validations.customer import *

# Create your views here.

class GetCustomersAPI(APIView):
    permission_classes = [IsCustomer]
    
    def get(self, request):
        keyword = request.GET.get('keyword', '')
        order_by = request.GET.get('order_by', 'id')
        page = int(request.GET.get('page', 1))
        pageSize = int(request.GET.get('pageSize', 10))

        try:
            m_data = Customer.objects.filter(Q(manager__user_info__name__contains=keyword) | Q(ads__contains=keyword) | Q(name__contains=keyword) | Q(phone__contains=keyword) | Q(email__contains=keyword) | Q(phone__contains=keyword)).order_by(order_by)
            serializer = CustomerSerializer(m_data[pageSize * (page - 1):pageSize * page], many=True)

            return Response({
                "data": serializer.data,
                "total": m_data.count()
            })
        except Exception as e:
            print(str(e))
            return Response("Internal Server Error", status=500)
        

class CreateCustomerAPI(APIView):
    permission_classes = [IsCustomer]
    
    def post(self, request):
        
        try:
            errors, status, clean_data = validate_create_customer(request)
            
            if status != 200:
                return Response({"errors": errors}, status=status)
            
            with transaction.atomic():
                customer = Customer.objects.create(
                    name=clean_data["last_name"] + " " + clean_data["first_name"],
                    last_name=clean_data["last_name"],
                    first_name=clean_data["first_name"],
                    email=clean_data["email"],
                    phone=clean_data["phone"],
                    email_2=clean_data["email_2"],
                    phone_2=clean_data["phone_2"],
                    ads=clean_data["ads"],
                    deposit_date=clean_data["deposit_date"],
                    contract_start_date=clean_data["contract_start_date"],
                    contract_days=clean_data["contract_days"],
                    status=Status.objects.filter(id=clean_data["status"]).first(),
                    property=Property.objects.filter(id=clean_data["property"]).first(),
                    system_provided=clean_data["system_provided"],
                    manager=request.user
                )

                return Response({
                    "msg": "顧客情報が正常に登録されました。",
                    "data": CustomerSerializer(customer).data
                })
        except Exception as e:
            print(str(e))
            return Response({"msg": "Internal Server Error"}, status=400)
        

class UpdateCustomerAPI(APIView):
    permission_classes = [IsCustomer]

    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        except Exception as e:
            print(str(e))
            return Response("Internal Server Error", status=500)
        

    def patch(self, request, customer_id):
        
        try:
            errors, status, clean_data = validate_update_customer(request, customer_id)
            
            if status != 200:
                return Response({"errors": errors}, status=status)
            
            with transaction.atomic():
                customer = Customer.objects.get(id=customer_id)
                customer.name = clean_data["last_name"] + " " + clean_data["first_name"]
                customer.last_name = clean_data["last_name"]
                customer.first_name = clean_data["first_name"]
                customer.email = clean_data["email"]
                customer.phone = clean_data["phone"]
                customer.email_2 = clean_data["email_2"]
                customer.phone_2 = clean_data["phone_2"]
                customer.ads = clean_data["ads"]
                customer.deposit_date = clean_data["deposit_date"]
                customer.contract_start_date = clean_data["contract_start_date"]
                customer.contract_days = clean_data["contract_days"]
                customer.status = Status.objects.filter(id=clean_data["status"]).first()
                customer.property = Property.objects.filter(id=clean_data["property"]).first()
                customer.system_provided = clean_data["system_provided"]
                customer.save()

                return Response({
                    "msg": "顧客情報が正常に更新されました。"
                })
        except Exception as e:
            print(str(e))
            return Response({"msg": "Internal Server Error"}, status=400)
        
    
    def delete(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            return Response({
                "msg": "顧客情報が正常に削除されました。"
            })
        except Exception as e:
            print(str(e))
            return Response({"msg": "Internal Server Error"}, status=400)