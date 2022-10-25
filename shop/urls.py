from django.urls import path, re_path

from shop.views import *


app_name = 'shop'

urlpatterns = [
    path('', product_list, name='product_list'),
    # re_path(r'^(?P<category_slug>[-\w]+)/$', product_list, name='product_list_by_category'),
    path('<slug:category_slug>/', product_list, name='product_list_by_category'),
    # re_path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', product_detail, name='product_detail'),
    path('<int:id>/<slug:slug>/', product_detail, name='product_detail'),
    path('/message/', post_message, name='post_message'),
]