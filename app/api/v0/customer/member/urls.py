
from django.conf.urls import include
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from .views.customer import *
from .views.memo import *
from .views.analysis import *
router = DefaultRouter()


urlpatterns = [
    re_path(r'^analysis/(?P<user_id>[0-9]+)$', GetUserAnalysisAPI.as_view(), name='get_user_analysis'),
    re_path(r'^customers/$', GetCustomersAPI.as_view(), name='get_customers'),
    re_path(r'^customers/create$', CreateCustomerAPI.as_view(), name='create_customer'),
    re_path(r'^customers/batch_create$', CreateMultiCustomerAPI.as_view(), name='create_multi_customer'),
    re_path(r'^customers/(?P<customer_id>[0-9]+)$', UpdateCustomerAPI.as_view(), name='update_customer'),
    re_path(r'^customers/(?P<customer_id>[0-9]+)/memo$', GetCustomerMemoAPI.as_view(), name='get_customer_memo'),
    re_path(r'^customers/(?P<customer_id>[0-9]+)/memo/create$', CreateCustomerMemoAPI.as_view(), name='create_customer_memo'),
    re_path(r'^customers/(?P<customer_id>[0-9]+)/memo/(?P<memo_id>[0-9]+)$', UpdateCustomerMemoAPI.as_view(), name='update_customer_memo'),

]
