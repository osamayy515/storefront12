import collections
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Collection, OrderItem, Product
from .serializers import CollectionSerializer, ProductSerializer

                #Generic view
class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
        #Only keeping this method because there is no default attribute for specifying the serializer context 
    def get_serializer_context(self):
        return {'request': self.request}

        #Only useful for giving some logic otherwise go with default queryset and serializer_class
    # def get_queryset(self):
        # return Product.objects.select_related('collection').all()
    # 
    # def get_serializer_class(self):
        # return ProductSerializer
    

                #class-based view
# class ProductList(APIView):
    # def get(self, request):
        # queryset = Product.objects.select_related('collection').all()
        # serializer = ProductSerializer(queryset, many=True, context={'request': request})
        # return Response(serializer.data)
# 
    # def post(self, request):
        # serializer = ProductSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)


                #Function-based view
# @api_view(['GET','POST'])
# def product_list(request):
    # 
    # if request.method == 'GET':
        # queryset = Product.objects.select_related('collection').all()
        # serializer = ProductSerializer(queryset, many=True, context={'request': request})
        # return Response(serializer.data)
    # 
    # elif request.method == 'POST':
        # serializer = ProductSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)

        
        #OR
        # if serializer.is_valid():
            # serializer.validated_data
            # return Response('ok')
        # else: 
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetails(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response({'error':'product cannot be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view(['GET','PUT','PATCH','DELETE'])
# def product_detail(request, id):
    # product = get_object_or_404(Product, pk=id)
    # 
    # if request.method == 'GET':
        # serializer = ProductSerializer(product)
        # return Response(serializer.data)
    # 
    # elif request.method == 'PUT':
        # serializer = ProductSerializer(product, data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)
    # 
    # elif request.method == 'DELETE':
        # if product.orderitems.count() > 0:
            # return Response({'error':'product cannot be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # product.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

# @api_view(['GET','POST'])
# def collection_list(request):
# 
    # if request.method == 'GET':
        # queryset = Collection.objects.annotate(products_count=Count('products')).all()
        # serializer = CollectionSerializer(queryset, many=True)
        # return Response(serializer.data)
    # 
    # elif request.method == 'POST':
        # serializer = CollectionSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET','PUT','PATCH','DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
    
    if request.method == 'GET':
        serializer = CollectionSerializer(collections)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error':'collection cannot be deleted because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    #OR

    # try:
        # product = Product.objects.get(pk=id)
        # serializer = ProductSerializer(product)
        # return Response(serializer.data)
    # except Product.DoesNotExist:
        # return Response(status=status.HTTP_404_NOT_FOUND)

