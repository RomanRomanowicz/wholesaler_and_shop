from django.urls import path, include, re_path
from orders.views import *

app_name = 'orders'

urlpatterns = [
    re_path(r'^create/$', order_create, name='order_create'),
    re_path(r'^admin/order/(?P<order_id>\d+)/$', admin_order_detail, name='admin_order_detail'),
]