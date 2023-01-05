# Generated by Django 4.1 on 2023-01-02 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productId', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('effectiveFrom', models.DateField(blank=True, null=True)),
                ('effectiveTo', models.DateField(blank=True, null=True)),
                ('lastUpdated', models.DateField()),
                ('productCategory', models.CharField(max_length=120)),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('brand', models.CharField(max_length=120)),
                ('brandName', models.CharField(blank=True, max_length=120, null=True)),
                ('applicationUri', models.TextField(blank=True, null=True)),
                ('isTailored', models.BooleanField()),
                ('additionalInformationOverviewUri', models.TextField(blank=True, null=True)),
                ('additionalInformationTermsUri', models.TextField(blank=True, null=True)),
                ('additionalInformationEligibilityUri', models.TextField(blank=True, null=True)),
                ('additionalInformationFeesAndPricingUri', models.TextField(blank=True, null=True)),
                ('additionalInformationBundleUri', models.TextField(blank=True, null=True)),
                ('additionalInfoAddOverviewUrisDesc', models.TextField(blank=True, null=True)),
                ('additionalInfoAddOverviewUrisAddInfoUri', models.TextField(blank=True, null=True)),
                ('additionalInfoAddTermsUrisDesc', models.TextField(blank=True, null=True)),
                ('additionalInfoAddTermsUrisAddlInfoUri', models.TextField(blank=True, null=True)),
                ('additionalInfoAddEligibilityUrisDesc', models.TextField(blank=True, null=True)),
                ('additionalInfoAddEligibilityUrisAddInfoUri', models.TextField(blank=True, null=True)),
                ('additionalInfoAddFeesAndPricingUrisDesc', models.TextField(blank=True, null=True)),
                ('additionalInfoAddFeesAndPricingUrisAddInfoUri', models.TextField(blank=True, null=True)),
                ('additionalInfoAddBundleUrisDesc', models.TextField(blank=True, null=True)),
                ('additionalInfoAddBundleUrisAddInfoUri', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LendingRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lendingRateType', models.CharField(max_length=120)),
                ('rate', models.CharField(max_length=120)),
                ('comparisonRate', models.CharField(blank=True, max_length=120, null=True)),
                ('calculationFrequency', models.CharField(blank=True, max_length=120, null=True)),
                ('applicationFrequency', models.CharField(blank=True, max_length=120, null=True)),
                ('interestPaymentDue', models.CharField(blank=True, max_length=120, null=True)),
                ('repaymentType', models.CharField(blank=True, max_length=120, null=True)),
                ('loanPurpose', models.CharField(blank=True, max_length=120, null=True)),
                ('tiersName', models.CharField(blank=True, max_length=120, null=True)),
                ('tiersUnitOfMeasure', models.CharField(blank=True, max_length=120, null=True)),
                ('tiersMinimumValue', models.CharField(blank=True, max_length=120, null=True)),
                ('tiersMaximumValue', models.CharField(blank=True, max_length=120, null=True)),
                ('tiersRateApplicationMethod', models.CharField(blank=True, max_length=120, null=True)),
                ('tiersApplicabilityConditionsAdditionalInfo', models.CharField(blank=True, max_length=120, null=True)),
                ('tiersApplicabilityConditionsAdditionalInfoUri', models.CharField(blank=True, max_length=120, null=True)),
                ('tiersAdditionalInfo', models.CharField(blank=True, max_length=120, null=True)),
                ('tiersAdditionalInfoUri', models.CharField(blank=True, max_length=120, null=True)),
                ('additionalValue', models.CharField(max_length=120)),
                ('additionalInfo', models.CharField(blank=True, max_length=120, null=True)),
                ('additionalInfoUri', models.CharField(blank=True, max_length=120, null=True)),
                ('insertTime', models.DateField()),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lendingRates', to='products.product')),
            ],
        ),
    ]
