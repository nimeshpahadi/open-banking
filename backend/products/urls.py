from django.urls import path, include, re_path
from products import views

urlpatterns = [
    re_path(r'^products$', views.getProducts),
    re_path(r'^products/create$', views.createProduct),
    re_path(r'^products/(?P<productId>.+)$', views.getProductDetails),
    re_path(r'^products/(?P<productId>[0-9]+)$', views.productUpdate),
]