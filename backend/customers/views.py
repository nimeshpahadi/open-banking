from django.shortcuts import render
from .serializers import CustomerSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.permissions import IsAuthenticated
from config import reusable_functions


@api_view()
@permission_classes([IsAuthenticated])
def getCustomers(request):
    hasHeaderError = reusable_functions.checkHeaderError(request)
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
        filterNullFromCustList = reusable_functions.cleanNullTerms(custDict)
        customerListData = {
            'data': filterNullFromCustList,
            'links': {'self': request.build_absolute_uri()},
            'meta': {}
        }
        return Response(customerListData, headers={'x-v': request.headers.get('x-v')})
    else:
        return hasHeaderError

@api_view()
@permission_classes([IsAuthenticated])
def getCustomerDetails(request):
    hasHeaderError = reusable_functions.checkHeaderError(request)
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
        filterNullFromCustList = reusable_functions.cleanNullTerms(custDict)
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