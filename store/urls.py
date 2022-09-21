from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view()),
    path('collections/', views.collection_list),
    path('products/<int:id>/', views.ProductDetails.as_view()),
    path('collections/<int:pk>/', views.collection_detail, name='collection-detail')
]
