from rest_framework import serializers
from .models import Product
from .models import LendingRate


class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = ('productId', 'effectiveFrom', 'effectiveTo', 'lastUpdated', 'productCategory', 'name', 'description',
              'brand', 'brandName', 'applicationUri', 'isTailored', 'additionalInformationOverviewUri', 
              'additionalInformationTermsUri', 'additionalInformationEligibilityUri', 
              'additionalInformationFeesAndPricingUri', 'additionalInformationBundleUri',
              'additionalInformationAdditionalOverviewUri', 'additionalInformationAdditionalTermsUri',
              'additionalInformationAdditionalEligibilityUri', 'additionalInformationAdditionalFeesAndPricingUri',
              'additionalInformationAdditionalBundleUri')

class LendingRateSerializer(serializers.ModelSerializer):
  class Meta:
    model = LendingRate
    fields = ('productId', 'lendingRateType', 'rate', 'comparisonRate', 'calculationFrequency', 
            'applicationFrequency', 'interestPaymentDue', 'repaymentType', 'loanPurpose', 'tiersName', 
            'tiersUnitOfMeasure', 'tiersMinimumValue', 'tiersMaximumValue', 'tiersRateApplicationMethod', 
            'tiersApplicabilityConditionsAdditionalInfo', 'tiersApplicabilityConditionsAdditionalInfoUri', 
            'tiersAdditionalInfo', 'tiersAdditionalInfoUri', 'additionalValue', 'additionalInfo', 
            'additionalInfoUri', 'insertTime')