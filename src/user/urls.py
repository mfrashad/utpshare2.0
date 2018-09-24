from django.conf.urls import url, include

from .views import UserDashboardView, OrderList, OrderDetail


urlpatterns = [
    url(r'^$', UserDashboardView.as_view(), name='user_dashboard'),
    url(r'^orders/$', OrderList.as_view(), name='orders'),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order_detail'),
]