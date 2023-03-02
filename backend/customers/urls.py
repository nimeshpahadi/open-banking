from django.urls import path, include, re_path
from customers import views

urlpatterns = [
    re_path(r'^common/customers$', views.getCustomers),
    # re_path(r'^products/create$', views.createProduct),
    re_path(r'^common/customer/detail', views.getCustomerDetails),
    # re_path(r'^products/(?P<productId>[0-9]+)$', views.productUpdate),
]