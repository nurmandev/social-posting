
from django.conf.urls import include
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views.customer import *
router = DefaultRouter()


urlpatterns = [
    re_path(r'^customers/$', GetCustomersAPI.as_view(), name='get_customers'),
    re_path(r'^customers/create$', CreateCustomerAPI.as_view(), name='create_customer'),
    re_path(r'^customers/(?P<customer_id>[0-9]+)$', UpdateCustomerAPI.as_view(), name='update_customer'),
]
