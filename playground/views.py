from itertools import count, product
from re import T
import django
from django.db.models import DecimalField
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Value, Func, Count, ExpressionWrapper
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.db.models.functions import Concat
from django.db import transaction
from django.db import connection
from django.contrib.contenttypes.models import ContentType
from store.models import Collection, Customer, Order, Product, OrderItem
from tags.models import TaggedItem


def say_hello(request):
    #To access the database directly
    # with connection.cursor() as cursor:
        # cursor.execute('')     #for executing raw SQL queries
        # cursor.callproc('')    #for executing stored procedures

    #OR
    # cursor = connection.cursor()
    # cursor.execute('')
    # cursor.close()

    #Running raw SQL querires
    # queryset = Product.objects.raw('select id, title from store_product')

    # ... (some code which is not required to be included in transaction)

    # with transaction.atomic():
        # order = Order()
        # order.customer_id = 1
        # order.save()

        # item = OrderItem()
        # item.order = order
        # item.product_id = 1
        # item.quantity = 1
        # item.unit_price = 10
        # item.save()

    # collection = Collection(pk=11)
    # collection.delete()

    # OR
    # Collection.objects.filter(id__gt=5).delete()
    
    
    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None           #but this will set the title to null or empty
    # collection.save()

    #OR
    # Collection.objects.filter(pk=11).update(featured_product=None)


    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=1) 
    # collection.save()
    # collection.id

    #OR
    # collection = Collection(title = 'abc', featured_product_id = 1)
    # collection.save()
    # collection.id

    #OR
    # collection.featured_product_id = 1
    # collection.save()
    # collection.id
    
    #OR
    # collection = Collection.objects.create(name='a', featured_product_id=1)
    # collection.save()
    # collection.id

    # queryset = Product.objects.all()
    # list(queryset)
    # queryset[0] #will use it from the queryset cache
    
    # queryset = TaggedItem.objects.get_tags_for(Product,1)

    # content_type = ContentType.objects.get_for_model(Product)
    # queryset = TaggedItem.objects \
        # .select_related('tag') \
        # .filter(
            # content_type = content_type,
            # object_id = 1
        # )

    # discounted_price = ExpressionWrapper(F('unit_price') * 0.8, output_field = DecimalField())
    # queryset = Product.objects.annotate(
        # discounted_price = discounted_price
    # )

    # queryset = Customer.objects.annotate(
        # orders_count = Count('order')
    # )

    # queryset = Customer.objects.annotate(
        # CONCAT
        # full_name = Concat('first_name', Value(' '), 'last_name')
    # )
    # queryset = Customer.objects.annotate(
        # CONCAT
        # full_name = Func(F('first_name'), Value(' '), F('last_name'), function= 'CONCAT')
    # )

    # queryset = Customer.objects.annotate(new_id = F('id'))
    # queryset = Customer.objects.annotate(is_new = Value(True))
    
    # result = Product.objects.filter(collection__id=3).aggregate(count = Count('id'), min_price = Min('unit_price'))

    # queryset = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    # select_related (1)
    # prefetch_related (n)
    # queryset = Product.objects.prefetch_related(
        # 'promotions').select_related('collection').all()
    
    # queryset = Product.objects.select_related('collection').all()
    
    # to be careful from
    # queryset = Product.objects.only('id', 'title')
    # queryset = Product.objects.defer('id', 'title')
    
    # queryset = Product.objects.filter(
        # id__in=OrderItem.objects.values('product__id').distinct()).order_by('title')
    # queryset = Product.objects.values_list('id','title','collection__title')
    # queryset = Product.objects.values('id','title','collection__title')
    
    # 5,6,7,8,9
    # queryset = Product.objects.all()[5:10]
    # 0,1,2,3,4
    # queryset = Product.objects.all()[:5]
    
    # product = Product.objects.order_by('unit_price')[1]
    # product = Product.objects.earliest('unit_price')
    # product = Product.objects.latest('unit_price')
    # queryset = Product.objects.order_by('unit_price','-title').reverse()
    # queryset = Product.objects.order_by('-title')
    # queryset = Product.objects.order_by('title')
    #products:
    # queryset = Product.objects.filter(inventory =F('collection__id'))
    # queryset = Product.objects.filter(inventory =F('unit_price'))
    # queryset = Product.objects.filter(
        # Q(inventory__lt=10) | ~Q(unit_price__lt=20))
    # queryset = Product.objects.filter(
        # Q(inventory__lt=10) | Q(unit_price__lt=20))
    # queryset = Product.objects.filter(
        # inventory__lt=10).filter(unit_price__lt=20)
    # queryset = Product.objects.filter(description__isnull=True)
    # queryset = Product.objects.filter(last_update__year=2021)
    # queryset = Product.objects.filter(title__iendswith='coffee')
    # queryset = Product.objects.filter(title__icontains='coffee')
    # queryset = Product.objects.filter(collection__id__range=(2,3))
    # queryset = Product.objects.filter(unit_price__range=(20,30))
    # for product in query_set:
    #      print(product)
    # list(query_set)
    # query_set[0:5]
    # return render(request, 'hello.html', {'name': 'Osama', 'result': list(queryset)})
    # return render(request, 'hello.html', {'name': 'Osama', 'tags': list(queryset)})
    return render(request, 'hello.html', {'name':'Osama'})
