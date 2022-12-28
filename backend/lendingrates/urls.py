from django.urls import path, include, re_path
from lendingrates import views

urlpatterns = [
    re_path(r'^api/lending-rates/$', views.lendingRateList),
    re_path(r'^api/lending-rates/(?P<pk>[0-9]+)$', views.lendingRateDetail),
]