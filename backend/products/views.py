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
    if isinstance(d, dict):
        return {
            k: v 
            for k, v in ((k, cleanNullTerms(v)) for k, v in d.items())
            if v
        }
    if isinstance(d, list):
        return [v for v in map(cleanNullTerms, d) if v]
    return d

def errorCode(code, title, detail):
    error = {
            "errors": [
                {
                    "code": "urn:au-cds:error:cds-all:" + code,
                    "title": title,
                    "detail": detail,
                    "meta": {}
                }
            ]
        }
    return error
def custom404(request, exception=None):
    error = {
            "errors": [
                {
                    "code": "urn:au-cds:error:cds-all:Resource/NotFound",
                    "title": "Resource Not Found",
                    "detail": "No matching route",
                    "meta": {}
                }
            ]
        }
    return Response(error, status=status.HTTP_404_NOT_FOUND)
@api_view()
def productDetail(request, productId):
    """Retrieve a product by pk - productId."""
    headerXVersion = request.headers.get("x-v")
    if not headerXVersion:
        code = "Header/Missing"
        title = "Missing Required Header"
        detail = "x-v"
        errorResponse = errorCode(code, title, detail)
        return Response(errorResponse, status=status.HTTP_400_BAD_REQUEST)
    if headerXVersion != "3":
        code = "Header/UnsupportedVersion"
        title = "Unsupported Version"
        detail = "Requested x-v version is not supported"
        errorResponse = errorCode(code, title, detail)
        return Response(errorResponse, status=status.HTTP_406_NOT_ACCEPTABLE)
    try:
        product = Product.objects.get(productId=productId)
    except Product.DoesNotExist:
        code = "Resource/Invalid"
        title = "Invalid Resource"
        detail = productId
        errorResponse = errorCode(code, title, detail)
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
        productList = []
        prodSerializer = ProductSerializer(products, context={'request': request}, many=True).data
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
        filterNullFromProductList = cleanNullTerms(productList)
        return Response(filterNullFromProductList)

    elif request.method == 'POST':
        prodSerializer = ProductSerializer(data=request.data)
        if prodSerializer.is_valid():
            prodSerializer.save()
            return Response(prodSerializer.data, status=status.HTTP_201_CREATED)
        return Response(prodSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

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