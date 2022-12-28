from django.db import models

class LendingRate(models.Model):
  productId = models.CharField(max_length=120)
  lendingRateType = models.CharField(max_length=120)
  rate = models.CharField(max_length=120)
  comparisonRate = models.CharField(max_length=120)
  calculationFrequency = models.CharField(max_length=120)
  applicationFrequency = models.CharField(max_length=120)
  interestPaymentDue = models.CharField(max_length=120)
  repaymentType = models.CharField(max_length=120)
  loanPurpose = models.CharField(max_length=120)
  tiersName = models.CharField(max_length=120)
  tiersUnitOfMeasure = models.CharField(max_length=120)
  tiersMinimumValue = models.CharField(max_length=120)
  tiersMaximumValue = models.CharField(max_length=120)
  tiersRateApplicationMethod = models.CharField(max_length=120)
  tiersApplicabilityConditionsAdditionalInfo = models.CharField(max_length=120)
  tiersApplicabilityConditionsAdditionalInfoUri = models.CharField(max_length=120)
  tiersAdditionalInfo = models.CharField(max_length=120)
  tiersAdditionalInfoUri = models.CharField(max_length=120)
  additionalValue = models.CharField(max_length=120)
  additionalInfo = models.CharField(max_length=120)
  additionalInfoUri = models.CharField(max_length=120)
  insertTime = models.DateField()

  def __str__(self):
    return self.rate