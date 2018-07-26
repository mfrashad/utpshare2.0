from django.urls import path

from .views import (
  ProductDetailView,
  ProductListView,
  ProductCreateView,
  )

app_name = 'utpshare'

urlpatterns = [
  path('', ProductListView.as_view(), name='products'),
  # path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
   path('create/', ProductCreateView.as_view(), name='product_create'),
  path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
 
]