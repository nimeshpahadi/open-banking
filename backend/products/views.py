from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Product
from .models import LendingRate
from .serializers import LendingRateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# function to filter the null value from the dictionary
def cleanNullTerms(d):
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = cleanNullTerms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean
@api_view()
def productDetail(request, productId):
    """Retrieve a product by pk - productId."""
    try:
        product = Product.objects.get(productId=productId)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    prodSerializer = ProductSerializer(product, context={'request': request}).data
    productDetail = {
        "productId": prodSerializer['productId'],
        "effectiveFrom": prodSerializer['effectiveFrom'],
        "effectiveTo": prodSerializer['effectiveTo'],
        "lastUpdated": prodSerializer['lastUpdated'],
        "productCategory": prodSerializer['productCategory'],
        "name": prodSerializer['name'],
        "description": prodSerializer['description'],
        "brand": prodSerializer['brand'],
        "brandName": prodSerializer['brandName'],
        "applicationUri": prodSerializer['applicationUri'],
        "isTailored": prodSerializer['isTailored'],
        "additionalInformation": {
            "overviewUri": prodSerializer['additionalInformationOverviewUri'],
            "termsUri": prodSerializer['additionalInformationTermsUri'],
            "eligibilityUri": prodSerializer['additionalInformationEligibilityUri'],
            "feesAndPricingUri": prodSerializer['additionalInformationFeesAndPricingUri'],
            "bundleUri": prodSerializer['additionalInformationBundleUri'],
        }
    }
    filterNullFromProductDetail = cleanNullTerms(productDetail)
    lRModal = LendingRate.objects.filter(productId=productId)
    lRSerializer = LendingRateSerializer(lRModal, context={'request': request}, many=True).data
    lendingRates = []
    checkDupLendRate = []
    depositRates = []
    tiersList = []
    for item in lRSerializer:
        lRDict = {
            "lendingRateType": item['lendingRateType'],
            "rate": item['rate'],
            "comparisonRate": item['comparisonRate'],
            "calculationFrequency": item['calculationFrequency'],
            "applicationFrequency": item['applicationFrequency'],
            "interestPaymentDue": item['interestPaymentDue'],
            "repaymentType": item['repaymentType'],
            "loanPurpose": item['loanPurpose'],
            "tiersName": item['tiersName'],
            "tiersUnitOfMeasure": item['tiersUnitOfMeasure'],
            "tiersRateApplicationMethod": item['tiersRateApplicationMethod'],
            "tiersApplicabilityConditionsAdditionalInfo": item['tiersApplicabilityConditionsAdditionalInfo'],
            "tiersApplicabilityConditionsAdditionalInfoUri": item['tiersApplicabilityConditionsAdditionalInfoUri'],
            "tiersAdditionalInfo": item['tiersAdditionalInfo'],
            "tiersAdditionalInfoUri": item['tiersAdditionalInfoUri'],
            "additionalValue": item['additionalValue'],
            "additionalInfo": item['additionalInfo'],
            "additionalInfoUri": item['additionalInfoUri'],
        }
        tiers = {
            "name": item['tiersName'],
            "unitOfMeasure": item['tiersUnitOfMeasure'],
            "minimumValue": item['tiersMinimumValue'],
            "maximumValue": item['tiersMaximumValue'],
            "rateApplicationMethod": item['tiersRateApplicationMethod'],
            "applicabilityConditions": {
                "additionalInfo": item['tiersApplicabilityConditionsAdditionalInfo'],
                "additionalInfoUri": item['tiersApplicabilityConditionsAdditionalInfoUri'],
            },
            "additionalInfo": item['tiersAdditionalInfo'],
            "additionalInfoUri": item['tiersAdditionalInfoUri'],
        }
        filterNullFromTiers = cleanNullTerms(tiers)
        formattedLendRate = {
            "lendingRateType": item['lendingRateType'],
            "rate": item['rate'],
            "comparisonRate": item['comparisonRate'],
            "calculationFrequency": item['calculationFrequency'],
            "applicationFrequency": item['applicationFrequency'],
            "interestPaymentDue": item['interestPaymentDue'],
            "repaymentType": item['repaymentType'],
            "loanPurpose": item['loanPurpose'],
        }
        filterNullFromLendingRate = cleanNullTerms(formattedLendRate)
        additionalData = {
            "additionalValue": item['additionalValue'],
            "additionalInfo": item['additionalInfo'],
            "additionalInfoUri": item['additionalInfoUri'],
        }
        filterNullFromAddData = cleanNullTerms(additionalData)
        if lRDict not in checkDupLendRate:
            checkDupLendRate.append(lRDict)
            tiersList = [filterNullFromTiers]
            filterNullFromLendingRate['tiers'] = tiersList
            for k, v in filterNullFromAddData.items():
                filterNullFromLendingRate[k] = v
            lendingRates.append(filterNullFromLendingRate)
        else:
            tiersList.append(filterNullFromTiers)

    filterNullFromProductDetail['depositRates'] = depositRates
    filterNullFromProductDetail['lendingRates'] = lendingRates
    product_data = {
        "data": filterNullFromProductDetail,
        "links": {"self": "https://openbank.api.mystate.com.au/cds-au/v1/banking/products/" + productId}
    }
    return Response(product_data)

@api_view(['GET', 'POST'])
def productList(request):
    """
 List  products, or create a new product.
 """
    if request.method == 'GET':
        products = Product.objects.all()

        serializer = ProductSerializer(products, context={'request': request}, many=True)
        
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['PUT', 'DELETE'])
def productUpdate(request, productId):
    try:
        product = Product.objects.get(pk=productId)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)