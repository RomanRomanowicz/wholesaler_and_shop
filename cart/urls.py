from django.urls import path, include, re_path
from cart.views import *

app_name = 'cart'

urlpatterns = [
    # re_path(r'^$', cart_detail, name='cart_detail'),
    path('', cart_detail, name='cart_detail'),
    # path('', CartDetail.as_view(), name='cart_detail'),
    # re_path(r'^add/(?P<product_id>\d+)/$', cart_add, name='cart_add'), ## stary wariant
    path('add/<int:product_id>/', cart_add, name='cart_add'),
    # re_path(r'^remove/(?P<product_id>\d+)/$', cart_remove, name='cart_remove'), ## stary wariant
    path('remove/<int:product_id>/', cart_remove, name='cart_remove'),
]