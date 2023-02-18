from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from products import views
from oauth.views import UserList, UserDetails, GroupList


urlpatterns = [
  path('admin/', admin.site.urls),
  path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
  path('users/', UserList.as_view()),
  path('users/<pk>/', UserDetails.as_view()),
  path('groups/', GroupList.as_view()),
  path('api/cds-au/v1/banking/', include('products.urls')),
  path('api/cds-au/v1/banking/', include('customers.urls')),
  path('contact/', include('contact.urls')),
  re_path(r'^.*$', views.resourceNotFoundError),
]

if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)