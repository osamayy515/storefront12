import collections
from dataclasses import fields
from rest_framework import serializers

from decimal import Decimal
from store.admin import ProductAdmin
from store.models import Customer, Product, Collection
from rest_framework import serializers

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','title']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        
        fields = ['id','title','unit_price','price_with_tax','collection']
        #OR
        # fields = '__all__'     #for showing all the fields but not a good practice

    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
        
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    #   #by hyperlink
    # collection = serializers.HyperlinkedRelatedField(
        # queryset = Collection.objects.all(),
        # view_name='collection-detail'
    # )
    
    #OR
    # by nested object
    # collection = CollectionSerializer()
    
    #OR
    # by string
    # collection = serializers.StringRelatedField() 
    
    #OR
    #by primarykey
    # collection = serializers.PrimaryKeyRelatedField(
        # queryset = Collection.objects.all()
    # )

    def calculate_tax(self, product:Product):
        return product.unit_price * Decimal(1.1)

    #validate example scenerio
    # def validate(self, data):
        # if data['password'] != data['confirm_password']:
            # return serializers.ValidationError('passwords do not match')
        # return data