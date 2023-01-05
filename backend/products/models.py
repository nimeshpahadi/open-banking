from django.db import models


class Product(models.Model):
  productId = models.CharField(max_length=120, primary_key=True)
  effectiveFrom = models.DateField(null=True, blank=True)
  effectiveTo = models.DateField(null=True, blank=True)
  lastUpdated = models.DateField()
  productCategory = models.CharField(max_length=120)
  name = models.CharField(max_length=120)
  description = models.TextField()
  brand = models.CharField(max_length=120)
  brandName = models.CharField(max_length=120, null=True, blank=True)
  applicationUri = models.TextField(null=True, blank=True)
  isTailored = models.BooleanField()
  additionalInformationOverviewUri = models.TextField(null=True, blank=True)
  additionalInformationTermsUri = models.TextField(null=True, blank=True)
  additionalInformationEligibilityUri = models.TextField(null=True, blank=True)
  additionalInformationFeesAndPricingUri = models.TextField(null=True, blank=True)
  additionalInformationBundleUri = models.TextField(null=True, blank=True)
  additionalInfoAddOverviewUrisDesc = models.TextField(null=True, blank=True)
  additionalInfoAddOverviewUrisAddInfoUri = models.TextField(null=True, blank=True)
  additionalInfoAddTermsUrisDesc = models.TextField(null=True, blank=True)
  additionalInfoAddTermsUrisAddlInfoUri = models.TextField(null=True, blank=True)
  additionalInfoAddEligibilityUrisDesc = models.TextField(null=True, blank=True)
  additionalInfoAddEligibilityUrisAddInfoUri = models.TextField(null=True, blank=True)
  additionalInfoAddFeesAndPricingUrisDesc = models.TextField(null=True, blank=True)
  additionalInfoAddFeesAndPricingUrisAddInfoUri = models.TextField(null=True, blank=True)
  additionalInfoAddBundleUrisDesc = models.TextField(null=True, blank=True)
  additionalInfoAddBundleUrisAddInfoUri = models.TextField(null=True, blank=True)

  def __str__(self):
    return self.productId

class LendingRate(models.Model):
  productId = models.ForeignKey(Product, related_name="lendingRates", on_delete=models.CASCADE)
  lendingRateType = models.CharField(max_length=120)
  rate = models.CharField(max_length=120)
  comparisonRate = models.CharField(max_length=120, null=True, blank=True)
  calculationFrequency = models.CharField(max_length=120, null=True, blank=True)
  applicationFrequency = models.CharField(max_length=120, null=True, blank=True)
  interestPaymentDue = models.CharField(max_length=120, null=True, blank=True)
  repaymentType = models.CharField(max_length=120, null=True, blank=True)
  loanPurpose = models.CharField(max_length=120, null=True, blank=True)
  tiersName = models.CharField(max_length=120, null=True, blank=True)
  tiersUnitOfMeasure = models.CharField(max_length=120, null=True, blank=True)
  tiersMinimumValue = models.CharField(max_length=120, null=True, blank=True)
  tiersMaximumValue = models.CharField(max_length=120, null=True, blank=True)
  tiersRateApplicationMethod = models.CharField(max_length=120, null=True, blank=True)
  tiersApplicabilityConditionsAdditionalInfo = models.CharField(max_length=120, null=True, blank=True)
  tiersApplicabilityConditionsAdditionalInfoUri = models.CharField(max_length=120, null=True, blank=True)
  tiersAdditionalInfo = models.CharField(max_length=120, null=True, blank=True)
  tiersAdditionalInfoUri = models.CharField(max_length=120, null=True, blank=True)
  additionalValue = models.CharField(max_length=120)
  additionalInfo = models.CharField(max_length=120, null=True, blank=True)
  additionalInfoUri = models.CharField(max_length=120, null=True, blank=True)
  insertTime = models.DateField()

  def __str__(self):
    return self.rate