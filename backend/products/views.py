from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Product
from .models import LendingRate
from .serializers import LendingRateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from config import reusable_functions


@api_view()
def getProducts(request):
    hasHeaderError = reusable_functions.checkHeaderError(request)
    if hasHeaderError == False:
        paginator = PageNumberPagination()
        paginator.page_size = 2
        products = Product.objects.all()
        result_page = paginator.paginate_queryset(products, request)
        productList = []
        prodSerializer = ProductSerializer(result_page, many=True).data
        #prodSerializer = ProductSerializer(products, context={'request': request}, many=True).data
        for item in prodSerializer:
            productDict = {
                "productId": item['productId'],
                "effectiveFrom": item['effectiveFrom'],
                "effectiveTo": item['effectiveTo'],
                "lastUpdated": item['lastUpdated'],
                "productCategory": item['productCategory'],
                "name": item['name'],
                "description": item['description'],
                "brand": item['brand'],
                "brandName": item['brandName'],
                "applicationUri": item['applicationUri'],
                "isTailored": item['isTailored'],
                "additionalInformation": {
                    "overviewUri": item['additionalInformationOverviewUri'],
                    "termsUri": item['additionalInformationTermsUri'],
                    "eligibilityUri": item['additionalInformationEligibilityUri'],
                    "feesAndPricingUri": item['additionalInformationFeesAndPricingUri'],
                    "bundleUri": item['additionalInformationBundleUri'],
                    "additionalOverviewUris": [
                        {
                            "additionalInfoUri": item['additionalInformationAdditionalOverviewUri']
                        }
                    ],
                    "additionalTermsUris": [
                        {
                            "additionalInfoUri": item['additionalInformationAdditionalTermsUri']
                        }
                    ],
                    "additionalEligibilityUris": [
                        {
                            "additionalInfoUri": item['additionalInformationAdditionalEligibilityUri']
                        }
                    ],
                    "additionalFeesAndPricingUris": [
                        {
                            "additionalInfoUri": item['additionalInformationAdditionalFeesAndPricingUri']
                        }
                    ],
                    "additionalBundleUris": [
                        {
                            "additionalInfoUri": item['additionalInformationAdditionalBundleUri']
                        }
                    ]
                }
            }
            productList.append(productDict)
        filterNullFromProductList = reusable_functions.cleanNullTerms(productList)
        links = {
            'self': request.build_absolute_uri(),
            'prev': paginator.get_previous_link(),
            'next': paginator.get_next_link()
        }
        filterNullFromLinks = reusable_functions.cleanNullTerms(links)
        productListData = {
            "data": {
                "products": filterNullFromProductList,
                "links": filterNullFromLinks,
                "meta": {
                    "totalRecords": paginator.page.paginator.count,
                    "totalPages": paginator.page_size
                }
            }
        }
        return Response(productListData, headers={'x-v': request.headers.get('x-v')})
    else:
        return hasHeaderError

@api_view(['POST'])
def createProduct(request):
    prodSerializer = ProductSerializer(data=request.data)
    if prodSerializer.is_valid():
        prodSerializer.save()
        return Response(prodSerializer.data, status=status.HTTP_201_CREATED)
    return Response(prodSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view()
def getProductDetails(request, productId):
    hasHeaderError = reusable_functions.checkHeaderError(request)
    if hasHeaderError == False:
        try:
            product = Product.objects.get(productId=productId)
        except Product.DoesNotExist:
            errorResponse = errorCode('Resource/Invalid', 'Invalid Resource', productId)
            return Response(errorResponse, status=status.HTTP_404_NOT_FOUND)
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
        filterNullFromProductDetail = reusable_functions.cleanNullTerms(productDetail)
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
            filterNullFromTiers = reusable_functions.cleanNullTerms(tiers)
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
            filterNullFromLendingRate = reusable_functions.cleanNullTerms(formattedLendRate)
            additionalData = {
                "additionalValue": item['additionalValue'],
                "additionalInfo": item['additionalInfo'],
                "additionalInfoUri": item['additionalInfoUri'],
            }
            filterNullFromAddData = reusable_functions.cleanNullTerms(additionalData)
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
        productDetailData = {
            "data": filterNullFromProductDetail,
            "links": {"self": request.build_absolute_uri()}
        }
        return Response(productDetailData, headers={'x-v': request.headers.get('x-v')})
    else:
        return hasHeaderError

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