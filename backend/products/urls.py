from django.urls import path, include, re_path
from products import views

urlpatterns = [
    re_path(r'^api/products/$', views.product_list),
    re_path(r'^api/products/(?P<product_id>.+)$', views.productDetail),
    re_path(r'^api/products/(?P<pk>[0-9]+)$', views.updateProduct),
]