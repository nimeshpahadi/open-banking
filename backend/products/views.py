# from rest_framework.generics import ListAPIView
# from rest_framework import permissions

# from .models import Product
# from .serializers import ProductSerializer


# class ProductListView(ListAPIView):
#   permission_classes = (permissions.AllowAny, )
#   queryset = Product.objects.all()
#   serializer_class = ProductSerializer
#   pagination_class = None

from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Product
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@api_view(['GET', 'POST'])
def product_list(request):
    """
 List  customers, or create a new customer.
 """
    if request.method == 'GET':
        #data = []
        products = Product.objects.all()

        serializer = ProductSerializer(products, context={'request': request}, many=True)
        
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    """
 Retrieve, update or delete a customer by id/pk.
 """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)