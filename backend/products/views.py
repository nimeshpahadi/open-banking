from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Product
from .models import LendingRate
from .serializers import LendingRateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view()
def productDetail(request, productId):
    """Retrieve a product by pk - productId."""
    try:
        product = Product.objects.get(productId=productId)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    productSerializer = ProductSerializer(product, context={'request': request}).data
    # for prod in productSerializer:
    #     productDetail = {
    #         "productId": prod['productId'],
    #         "lastUpdated": prod['lastUpdated'],
    #         "productCategory": prod['productCategory'],
    #         "name": prod['name'],
    #         "description": prod['description'],
    #         "brand": prod['brand'],
    #         "applicationUri": prod['applicationUri'],
    #         "additionalInformation": {
    #             "overviewUri": prod['additionalInformationOverviewUri'],
    #             "termsUri": prod['additionalInformationTermsUri'],
    #             "eligibilityUri": prod['additionalInformationEligibilityUri'],
    #             "feesAndPricingUri": prod['additionalInformationFeesAndPricingUri'],
    #             "bundleUri": prod['additionalInformationBundleUri'],
    #         }
    #     }
    lRModal = LendingRate.objects.filter(productId=productId)
    lRSerializer = LendingRateSerializer(lRModal, context={'request': request}, many=True).data
    lendingRates = []
    checkDupLendRate = []
    depositRates = []
    tierList = []
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
        }
        tiers = {
            "name": item['tiersName'],
            "unitOfMeasure": item['tiersUnitOfMeasure'],
            "minimumValue": item['tiersMinimumValue'],
            "maximumValue": item['tiersMaximumValue'],
            "rateApplicationMethod": item['tiersRateApplicationMethod'],
        }
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
        if lRDict not in checkDupLendRate:
            checkDupLendRate.append(lRDict)
            tierList = [tiers]
            formattedLendRate.update({"tiers": tierList})
            lendingRates.append(formattedLendRate)
        else:
            tierList.append(tiers)

    productSerializer.update({"depositRates": depositRates})
    productSerializer.update({"lendingRates": lendingRates})
    product_data = {
        "data": productSerializer,
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