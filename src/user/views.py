import random

from django.views.generic import View
from django.views.generic.detail import DetailView
from django.shortcuts import render

# Create your views here.

from utpshare.mixins import LoginRequiredMixin
from products.models import Product
from orders.models import Order

class UserDashboardView(View):
  def get(self, request, *args, **kwargs):
    tag_views = None
    products = None
    top_tags = None
    owned = None
    try:
      tag_views = request.user.tagview_set.all().order_by("-count")[:5]
    except:
      pass

    if tag_views:
      top_tags = [x.tag for x in tag_views]
      products = Product.objects.filter(tags__in=top_tags)
      products=products.distinct()
      products = sorted(products, key= lambda x: random.random())
      products = products[:8]

    #  ORDER LIST
    order_id = self.request.session.get("order_id")
    try:
      user_orders = Order.objects.filter(user=request.user).filter(status="completed").order_by("-time_created")[:2]
    except:
      user_orders = None

    context = {
      "products": products,
      "top_tags": top_tags,
      "user": request.user,
      "order_id": order_id,
      "user_orders": user_orders,
    }
    return render(request, "user/dashboard.html", context)



class OrderList(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    order_id = self.request.session.get("order_id")
    try:
      user_orders = Order.objects.filter(user=request.user).order_by("-time_created")
    except:
      user_orders = None

    context = {
      "user_orders": user_orders,
      "order_id": order_id,
    }
    return render(request, "user/order_list.html", context)


class OrderDetail(DetailView):
  model = Order
  template_name = "user/order_detail.html"

  def dispatch(self, request, *args, **kwargs):
    obj = self.get_object()
    if obj.user == request.user and request.user is not None:
      return super(OrderDetail, self).dispatch(request, *args, **kwargs)
    else:
      raise Http404