from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from products import views

urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/cds-au/v1/banking/', include('products.urls')),
  path('contact/', include('contact.urls')),
  re_path(r'^.*$', views.resourceNotFoundError),
]

if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)