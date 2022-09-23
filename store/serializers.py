from dataclasses import fields
from rest_framework import serializers
from decimal import Decimal
from store.models import Customer, Product, Collection, Review
from rest_framework import serializers

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title','products_count']

    products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        
        fields = ['id','title','description','slug','inventory','unit_price','price_with_tax','collection']
        # depth = 1
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

    # def create(self, validated_data):
        # product = Product(**validated_data)
        # product.other = 1
        # product.save()
        # return product
# 
    # def update(self, instance, validated_data):
        # instance.unit_price = validated_data.get('unit_price')
        # instance.save()
        # return instance

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','date','name','description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)