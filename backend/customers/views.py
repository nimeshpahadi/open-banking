from django.shortcuts import render
from .serializers import CustomerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer


# filter null value from the dictionary
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

# generic format for 4xx errors
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

# handle all combination of headers error
def checkHeaderError(request):
    headerXV = request.headers.get('x-v')
    if 'x-v' not in request.headers:
        errorResponse = errorCode('Header/Missing', 'Missing Required Header', 'x-v')
        return Response(errorResponse, status=status.HTTP_400_BAD_REQUEST)
    elif headerXV == "" or headerXV.isdigit() == False:
        errorResponse = errorCode('Header/InvalidVersion', 'Invalid Version', 'Invalid x-v Requested')
        return Response(errorResponse, status=status.HTTP_400_BAD_REQUEST)
    elif headerXV != "3":
        errorResponse = errorCode('Header/UnsupportedVersion', 'Unsupported Version', 'Requested x-v version is not supported')
        return Response(errorResponse, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return False

@api_view()
def getCustomers(request):
    hasHeaderError = checkHeaderError(request)
    if hasHeaderError == False:
        customers = Customer.objects.all()
        custSerializer = CustomerSerializer(customers, many=True).data        
        for item in custSerializer:
            custDict = {
                "customerUType": item['customer_utype'],
                "person": {
                    "lastUpdateTime": item['last_update_time'],
                    "firstName": item['person_first_name'],
                    "lastName": item['person_last_name'],
                    "middleNames": [item['person_middle_name1']],
                    "prefix": item['person_prefix']
                }
            }
        filterNullFromCustList = cleanNullTerms(custDict)
        customerListData = {
            'data': filterNullFromCustList,
            'links': {'self': request.build_absolute_uri()},
            'meta': {}
        }
        return Response(customerListData, headers={'x-v': request.headers.get('x-v')})
    else:
        return hasHeaderError

# @api_view(['POST'])
# def createCust(request):
#     custSerializer = ProductSerializer(data=request.data)
#     if prodSerializer.is_valid():
#         prodSerializer.save()
#         return Response(prodSerializer.data, status=status.HTTP_201_CREATED)
#     return Response(prodSerializer.errors, status=status.HTTP_400_BAD_REQUEST)