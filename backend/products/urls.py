from django.urls import path, include, re_path
from products import views

urlpatterns = [
    re_path(r'^api/products/$', views.productList),
    re_path(r'^api/products/(?P<productId>.+)$', views.productDetail),
    re_path(r'^api/products/(?P<productId>[0-9]+)$', views.productUpdate),
]