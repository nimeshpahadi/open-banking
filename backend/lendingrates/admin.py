from django.contrib import admin
from .models import LendingRate


class LendingRateAdmin(admin.ModelAdmin):
  search_fields = ('repaymentType', 'calculationFrequency')
  list_per_page = 20

admin.site.register(LendingRate, LendingRateAdmin)
