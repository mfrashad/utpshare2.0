from django.conf.urls import url

from .views import (
  ProductDetailView,
  ProductListView,
  TagListView,
  TagDetailView,
  )

# app_name = 'utpshare'

# urlpatterns = [
#   path('', ProductListView.as_view(), name='products'),
#   # path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
#   path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
# ]


urlpatterns = [
  url(r'^$', ProductListView.as_view(), name='products'),
  url(r'^detail/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='product_detail'),
  url(r'^tags/$', TagListView.as_view(), name='tags'),
  url(r'^tags/(?P<slug>[\w-]+)/$', TagDetailView.as_view(), name='tag_detail'),
]