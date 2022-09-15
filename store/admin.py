from urllib.parse import urlencode
from django.http import HttpResponse
from django.contrib import admin, messages
from django.db.models import Count
from django.db.models import F
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<10','Low')
        ]
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['title','unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection','last_update',InventoryFilter]
    list_per_page = 20
    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title
        
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.SUCCESS
        )

# admin.site.register(models.Product, ProductAdmin)      #no longer needed because of line 4

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)}))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super(CollectionAdmin, self).get_queryset(request).annotate(
            products_count=Count(F('product')))


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership','orders_count']
    list_editable = ['membership']
    list_per_page = 20
    search_fields = ['first_name__istartswith','last_name__istartswith']
    
    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        return customer.orders_count
        # url = (reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(customer.id)}))
        # return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super(CustomerAdmin, self).get_queryset(request).annotate(
            orders_count=Count(F('order')))


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','customer']


