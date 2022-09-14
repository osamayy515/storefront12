from django.contrib import admin
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','unit_price','inventory_status']
    list_editable = ['unit_price']
    list_per_page = 20

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
# admin.site.register(models.Product, ProductAdmin)      #no longer needed because of line 4

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership']
    list_editable = ['membership']
    list_per_page = 20


admin.site.register(models.Collection)