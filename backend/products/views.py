from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Product
from lendingrates.models import LendingRate
from lendingrates.serializers import LendingRateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view()
def productDetail(request, product_id):
    """Retrieve a product by pk - product_id."""
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    productSerializer = ProductSerializer(product, context={'request': request}).data
    lRModal = LendingRate.objects.filter(productId=product_id)
    lRSerializer = LendingRateSerializer(lRModal, context={'request': request}, many=True).data
    result = {}
    lendingRates = []
    depositRates = []
    for item in lRSerializer:
        rate = item['rate']
        tiers = {
            "name": item['tiersName'],
            "unitOfMeasure": item['tiersUnitOfMeasure'],
            "minimumValue": item['tiersMinimumValue'],
            "maximumValue": item['tiersMaximumValue'],
            "rateApplicationMethod": item['tiersRateApplicationMethod'],
        }
        if result.get(rate):
            result[rate].append(tiers)
        else:
            result[rate] = [tiers]

    for key, value in result.items():
        for item in lRSerializer:
            if key == item['rate']:
                lRDict = {
                "lendingRateType": item['lendingRateType'],
                "rate": item['rate'],
                "comparisonRate": item['comparisonRate'],
                "calculationFrequency": item['calculationFrequency'],
                "applicationFrequency": item['applicationFrequency'],
                "interestPaymentDue": item['interestPaymentDue'],
                "repaymentType": item['repaymentType'],
                "loanPurpose": item['loanPurpose'],
                "tiers": value
            }
        lendingRates.append(lRDict)

    productSerializer.update({"depositRates": depositRates})
    productSerializer.update({"lendingRates": lendingRates})
    product_data = {
        "data": productSerializer,
        "links": {"self": "https://openbank.api.mystate.com.au/cds-au/v1/banking/products/" + product_id}
    }
    return Response(product_data)

@api_view(['GET', 'POST'])
def product_list(request):
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
def updateProduct(request, pk):
    try:
        product = Product.objects.get(pk=pk)
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