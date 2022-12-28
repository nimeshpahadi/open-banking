from django.shortcuts import render
from rest_framework import viewsets
from .serializers import LendingRateSerializer
from .models import LendingRate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@api_view(['GET', 'POST'])
def lendingRateList(request):
    """
 List  lending rates, or create a new lending rate.
 """
    if request.method == 'GET':
        lendingRate = LendingRate.objects.all()

        serializer = LendingRateSerializer(lendingRate, context={'request': request}, many=True)
        
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LendingRateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def lendingRateDetail(request, pk):
    """
 Retrieve, update or delete a lending rate by id/pk.
 """
    try:
        lendingRate = LendingRate.objects.get(pk=pk)
    except LendingRate.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LendingRateSerializer(lendingRate, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LendingRateSerializer(lendingRate, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        lendingRate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)