from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
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
        manager = int(request.GET.get('manager', 0))
        status = int(request.GET.get('status', 0))
        property = int(request.GET.get('property', 0))
        page = int(request.GET.get('page', 1))
        pageSize = int(request.GET.get('pageSize', 10))

        try:
            m_data = Customer.objects.filter(Q(manager__user_info__name__contains=keyword) | Q(ads__contains=keyword) | Q(name__contains=keyword) | Q(phone__contains=keyword) | Q(email__contains=keyword) | Q(phone__contains=keyword))

            role = get_role(request.user)
            
            if role == "admin":
                if manager != 0:
                    m_data = m_data.filter(manager=User.objects.filter(id=manager).first())
            elif role == "member":
                m_data = m_data.filter(manager=request.user)
            else:
                raise Exception("Forbidden")
                
            if Status.objects.filter(id=status).exists():
                m_data = m_data.filter(status=Status.objects.filter(id=status).first())

            if Property.objects.filter(id=property).exists():
                m_data = m_data.filter(property=Property.objects.filter(id=property).first())

            m_data = m_data.order_by(order_by)
            
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
        


class CreateBatchCustomerAPI(APIView):
    permission_classes = [IsCustomer]
    
    def post(self, request):
        data = dict(request.data)

        try:
            res = []
            customers = data.get('data', [])

            for customer in customers:
                name = customer.get('name', '')
                if len(name.split(' ')) == 2:
                    last_name = name.split(' ')[0]
                    first_name = name.split(' ')[1]
                else:
                    last_name = name
                    first_name = ''
                email = customer.get('email', '')
                phone = customer.get('phone', '')
                email_2 = customer.get('email_2', '')
                phone_2 = customer.get('phone_2', '')
                ads = customer.get('ads', '')
                deposit_date = customer.get('deposit_date', None)
                contract_start_date = customer.get('contract_start_date', None)

                try:
                    contract_days = int(customer.get('contract_days', 0))
                except:
                    contract_days = 0
                    
                status = customer.get('status', '')
                property = customer.get('property', '')
                system_provided = customer.get('system_provided', "NG")

                try:
                    role = get_role(request.user)
                    if role == "member":
                        manager= request.user
                    elif role == "admin":
                        manager = User.objects.filter(user_info__name=customer.get('manager', '')).first()
                        if manager is None:
                            raise Exception("Invalid Data")
                    
                    if name == "" or email == "" or phone == "" or Customer.objects.filter(email=email).exists():
                        raise Exception("Invalid Data")

                    with transaction.atomic():
                        # get last name and first name from name

                        m_customer = Customer.objects.create(
                            name = name,
                            last_name = last_name,
                            first_name = first_name,
                            email = email,
                            phone = phone,
                            email_2 = email_2,
                            phone_2 = phone_2,
                            ads = ads,
                            deposit_date = deposit_date,
                            contract_start_date = contract_start_date,
                            contract_days = contract_days,
                            status = Status.objects.filter(Q(status_type=status)|Q(name=status)).first(),
                            property = Property.objects.filter(Q(property_type=property)|Q(name=property)).first(),
                            system_provided = True if system_provided == "OK" else False,
                            manager = manager
                        )

                        res.append({
                            "data": customer,
                            "status": 200
                        })
                except Exception as e:
                    print(str(e))
                    res.append({
                        "data": customer,
                        "status": 400
                    })


            return Response(res)
        except Exception as e:
            print(str(e))
            return Response({"msg": "Internal Server Error"}, status=400)
        

class UpdateCustomerAPI(APIView):
    permission_classes = [IsCustomer]

    def get(self, request, customer_id):
        try:
            customer = Customer.objects.filter(id=customer_id)

            role = get_role(request.user)
            if role == "member":
                customer = customer.filter(manager=request.user)
            elif role == "admin":
                pass
            else:
                raise Exception("Forbidden")

            customer = customer.first()
            
            if customer is None:
                raise Exception("データが見つかりません。")
            
            serializer = CustomerFlatSerializer(customer)
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
            errors, status, clean_data = validate_delete_customer(request, customer_id)
            
            if status != 200:
                return Response({"errors": errors}, status=status)
            
            customer = Customer.objects.get(id=customer_id)
            customer.delete()

            return Response({
                "msg": "顧客情報が正常に削除されました。"
            })
        except Exception as e:
            print(str(e))
            return Response({"msg": "Internal Server Error"}, status=400)
        

class DownloadCustomerAPI(APIView):
    permission_classes = [IsCustomer]
    
    def get(self, request):
        try:
            customers = Customer.objects.all()

            role = get_role(request.user)
            if role == "member":
                customers = customers.filter(manager=request.user)
            
            import os
            import xlsxwriter
            from uuid import uuid4
            import datetime
            
            if not os.path.exists(f"storage/customers"):
                os.makedirs(f"storage/customers")

            path = f"storage/customers/{uuid4()}.xlsx"

            workbook = xlsxwriter.Workbook(path)
            worksheet = workbook.add_worksheet()

            font_format = workbook.add_format({'font_name': 'Yu Mincho'})
            row = 0
            worksheet.write(row, 0, "広告媒体", font_format)
            worksheet.write(row, 1, "氏名", font_format)
            worksheet.write(row, 2, "メールアドレス", font_format)
            worksheet.write(row, 3, "電話番号", font_format)
            worksheet.write(row, 4, "メールアドレス2", font_format)
            worksheet.write(row, 5, "電話番号2", font_format)
            if role == "admin":
                worksheet.write(row, 6, "担当者", font_format)
                worksheet.write(row, 7, "入金日", font_format)
                worksheet.write(row, 8, "契約開始日", font_format)
                worksheet.write(row, 9, "契約日数", font_format)
                worksheet.write(row, 10, "属性", font_format)
                worksheet.write(row, 11, "ステータス", font_format)
                worksheet.write(row, 12, "システム提供", font_format)
            else:
                worksheet.write(row, 6, "入金日", font_format)
                worksheet.write(row, 7, "契約開始日", font_format)
                worksheet.write(row, 8, "契約日数", font_format)
                worksheet.write(row, 9, "属性", font_format)
                worksheet.write(row, 10, "ステータス", font_format)
                worksheet.write(row, 11, "システム提供", font_format)

            row += 1

            for customer in customers:
                worksheet.write(row, 0, customer.ads, font_format)
                worksheet.write(row, 1, customer.name, font_format)
                worksheet.write(row, 2, customer.email, font_format)
                worksheet.write(row, 3, customer.phone, font_format)
                worksheet.write(row, 4, customer.email_2, font_format)
                worksheet.write(row, 5, customer.phone_2, font_format)
                if role == "admin":
                    worksheet.write(row, 6, customer.manager.user_info.name, font_format)
                    worksheet.write(row, 7, datetime.datetime.strftime(customer.deposit_date, "%Y-%m-%d") if customer.deposit_date else "", font_format)
                    worksheet.write(row, 8, datetime.datetime.strftime(customer.contract_start_date, "%Y-%m-%d") if customer.contract_start_date else "", font_format)
                    worksheet.write(row, 9, customer.contract_days, font_format)
                    worksheet.write(row, 10, customer.property.property_type if customer.property else "", font_format)
                    worksheet.write(row, 11, customer.status.status_type if customer.status else "", font_format)
                    worksheet.write(row, 12, "OK" if customer.system_provided else "NG", font_format)
                else:
                    worksheet.write(row, 6, datetime.datetime.strftime(customer.deposit_date, "%Y-%m-%d") if customer.deposit_date else "", font_format)
                    worksheet.write(row, 7, datetime.datetime.strftime(customer.contract_start_date, "%Y-%m-%d") if customer.contract_start_date else "", font_format)
                    worksheet.write(row, 8, customer.contract_days, font_format)
                    worksheet.write(row, 9, customer.property.property_type if customer.property else "", font_format)
                    worksheet.write(row, 10, customer.status.status_type if customer.status else "", font_format)
                    worksheet.write(row, 11, "OK" if customer.system_provided else "NG", font_format)
                
                row += 1
            workbook.close()

            return FileResponse(open(path, 'rb'), status=200)
        except Exception as e:
            print(str(e))
            return Response("Internal Server Error", status=500)