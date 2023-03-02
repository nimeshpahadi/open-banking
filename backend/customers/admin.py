from django.contrib import admin
from .models import Customer
from .models import CustomerPhoneNumber
from .models import CustomerPhysicalAddress


class CustomerAdmin(admin.ModelAdmin):
  list_display = ('customer_number', 'person_last_name', 'customer_utype', 'purpose')
  list_display_links = ('customer_number', 'person_last_name')
  search_fields = ('customer_number', 'person_last_name')
  list_per_page = 20

class CustomerPhoneNumberAdmin(admin.ModelAdmin):
  list_display = ('full_number', 'purpose')
  #list_display_links = ('full_number', 'number')
  search_fields = ('full_number', 'number')
  list_per_page = 20

class CustomerPhysicalAddressAdmin(admin.ModelAdmin):
  list_display = ('simple_address_line1', 'address_utype', 'purpose')
  #list_display_links = ('simple_address_line1', 'last_modified_time')
  search_fields = ('simple_address_line1', 'simple_mailing_name')
  list_per_page = 20

admin.site.register(Customer, CustomerAdmin)
admin.site.register(CustomerPhoneNumber, CustomerPhoneNumberAdmin)
admin.site.register(CustomerPhysicalAddress, CustomerPhysicalAddressAdmin)