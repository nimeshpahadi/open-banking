from django.contrib import admin
from .models import Product
from .models import LendingRate


class ProductAdmin(admin.ModelAdmin):
  list_display = ('productId', 'name')
  list_display_links = ('productId', 'name')
  search_fields = ('name', 'description')
  list_per_page = 20

class LendingRateAdmin(admin.ModelAdmin):
  search_fields = ('productId', 'rate')
  list_per_page = 20

admin.site.register(Product, ProductAdmin)
admin.site.register(LendingRate, LendingRateAdmin)