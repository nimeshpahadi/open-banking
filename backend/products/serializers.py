from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = ('product_id', 'effective_from', 'effective_to', 'last_updated',
            'product_category', 'name', 'description', 'brand', 'brand_name', 'application_uri',
            'is_tailored', 'additional_information_overview_uri', 'additional_information_terms_uri',
            'additional_information_eligibility_uri', 'additional_information_fees_and_pricing_uri',
            'additional_information_bundle_uri')