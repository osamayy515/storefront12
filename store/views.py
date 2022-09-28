from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from .pagination import DefaultPagination
from .filters import ProductFilter
from .models import Cart, CartItem, Collection, OrderItem, Product, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, ProductSerializer, ReviewSerializer
                
                #Product Viewset
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    # pagination_class = PageNumberPagination
    search_fields = ['title','description']
    ordering_fields = ['unit_price','last_update']

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error':'product cannot be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

                #Collection Viewset
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error':'collection cannot be deleted because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

                #Review Viewset
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

                #Generic view
# class ProductList(ListCreateAPIView):
    # queryset = Product.objects.select_related('collection').all()
    # serializer_class = ProductSerializer

        #Only keeping this method because there is no default attribute for specifying the serializer context 
    # def get_serializer_context(self):
        # return {'request': self.request}

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

# class ProductDetails(RetrieveUpdateDestroyAPIView):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    # lookup_field = 'id'
# 
    # def delete(self, request, pk):
        # product = get_object_or_404(Product, pk=pk)
        # if product.orderitems.count() > 0:
            # return Response({'error':'product cannot be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # product.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductDetails(APIView):
    # def get(self, request, id):
        # product = get_object_or_404(Product, pk=id)
        # serializer = ProductSerializer(product)
        # return Response(serializer.data)
# 
    # def put(self, request, id):
        # product = get_object_or_404(Product, pk=id)
        # serializer = ProductSerializer(product, data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)
# 
    # def delete(self, request, id):
        # product = get_object_or_404(Product, pk=id)
        # if product.orderitems.count() > 0:
            # return Response({'error':'product cannot be deleted because it is associated with an order item.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # product.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)



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


                #Collection generic view
# class CollectionList(ListCreateAPIView):
    # queryset = Collection.objects.annotate(products_count=Count('products')).all()
    # serializer_class = CollectionSerializer

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

                #Collection generic view
# class CollectionDetails(RetrieveUpdateDestroyAPIView):
    # queryset = Collection.objects.annotate(products_count=Count('products'))
    # serializer_class = CollectionSerializer
# 
    # def delete(self, request, pk):
        # collection = get_object_or_404(Collection, pk=pk)
        # if collection.products.count() > 0:
            # return Response({'error':'collection cannot be deleted because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # collection.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET','PUT','PATCH','DELETE'])
# def collection_details(request, pk):
    # collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
    # 
    # if request.method == 'GET':
        # serializer = CollectionSerializer(collections)
        # return Response(serializer.data)
    # 
    # elif request.method == 'PUT':
        # serializer = CollectionSerializer(collection, data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # return Response(serializer.data)
    # 
    # elif request.method == 'DELETE':
        # if collection.products.count() > 0:
            # return Response({'error':'collection cannot be deleted because it includes one or more products.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # collection.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)


    #OR

    # try:
        # product = Product.objects.get(pk=id)
        # serializer = ProductSerializer(product)
        # return Response(serializer.data)
    # except Product.DoesNotExist:
        # return Response(status=status.HTTP_404_NOT_FOUND)

