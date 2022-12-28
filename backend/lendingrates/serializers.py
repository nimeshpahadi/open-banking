from rest_framework import serializers
from .models import LendingRate


class LendingRateSerializer(serializers.ModelSerializer):
  class Meta:
    model = LendingRate
    fields = ('id' ,'productId', 'lendingRateType', 'rate', 'comparisonRate',
            'calculationFrequency', 'applicationFrequency', 'interestPaymentDue', 'repaymentType',
            'loanPurpose', 'tiersName', 'tiersUnitOfMeasure',
            'tiersMinimumValue', 'tiersMaximumValue', 'tiersRateApplicationMethod', 'tiersApplicabilityConditionsAdditionalInfo',
            'tiersApplicabilityConditionsAdditionalInfoUri', 'tiersAdditionalInfo', 'tiersAdditionalInfoUri',
            'additionalValue', 'additionalInfo', 'additionalInfoUri', 'insertTime')