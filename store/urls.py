from cgitb import lookup
from itertools import product
from xml.etree.ElementInclude import include
from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views
from pprint import pprint

router = routers.DefaultRouter()
router.register('products',views.ProductViewSet, basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet)
router.register('customers',views.CustomerViewSet)
router.register('orders',views.OrderViewSet, basename='orders')
# pprint(router.urls)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_routers = routers.NestedDefaultRouter(router , 'carts', lookup='cart')
carts_routers.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + products_router.urls + carts_routers.urls

# urlpatterns = [
    # path(r'', include(router.urls)),
    # path(r'', include(products_router.urls)),
    # path('products/', views.ProductList.as_view()),
    # path('collections/', views.CollectionList.as_view()),
    # path('products/<int:pk>/', views.ProductDetails.as_view()),
    # path('collections/<int:pk>/', views.CollectionDetails.as_view(), name='collection-detail')
# ]
