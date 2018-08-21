from django.conf.urls import url
from seller import views

from .views import (
        SellerDashboard,
        SellerProductListView,
        SellerProductDetailRedirectView,
        SellerTransactionListView,
        ProductCreateView,
        ProductUpdateView,
        )

# app_name = 'utpshare'

urlpatterns = [
  url(r'^$', SellerDashboard.as_view(), name='dashboard'),
  url(r'^transactions/$', SellerTransactionListView.as_view(), name='transactions'),
  url(r'^products/$', SellerProductListView.as_view(), name='product_list'),
  url(r'^products/add/$', ProductCreateView.as_view(), name='product_create'),
  url(r'^products/(?P<slug>[\w-]+)/edit/$', ProductUpdateView.as_view(), name='product_update'),
  
  url(r'^products/modal_add/$', views.product_create, name='modal_product_create'),
  url(r'^products/(?P<slug>[\w-]+)/modal_edit/$', views.product_update, name='modal_product_update'),
  url(r'^products/(?P<slug>[\w-]+)/modal_delete/$', views.product_delete, name='modal_product_delete'),
  
]


'''
The urlpattern below is going to break any url which comes after it
and has the pattern "products/*char*/
Ex. products/add
Ex.2 products/modal_add
WHY? Because slug can arguably be any word possible, so django will search for it,
hence break any further patterns

DANGER! DON'T USE THIS PATTERN!
path('products/<slug:slug>/', SellerProductDetailRedirectView.as_view()),
'''