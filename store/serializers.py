from rest_framework import serializers
from decimal import Decimal
from store.models import Cart, CartItem, Customer, Product, Collection, Review
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

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given ID was found.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            # updating existing item
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # creating new item
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(read_only=True, many=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, cart:Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items','total_price']
