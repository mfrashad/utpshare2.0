import random

from django.views.generic import View
from django.views.generic.detail import DetailView
from django.shortcuts import render

# Create your views here.

from utpshare.mixins import LoginRequiredMixin
from products.models import Product
from orders.models import UserCheckout, Order

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

      if products.count() <= 5:
        products = Product.objects.all().order_by("?")
        products = products[:8]
      else:
        products=products.distinct()
        products = sorted(products, key= lambda x: random.random())
        products = products[:8]

    context = {
      "products": products,
      "top_tags": top_tags,
    }
    return render(request, "user/dashboard.html", context)



class OrderList(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    user_email = request.user.email
    try:
      user_checkout = UserCheckout.objects.get(email=user_email)
      user_orders = Order.objects.filter(user=user_checkout).order_by("-time_created")
    except:
      user_orders = None

    context = {
      "user_orders": user_orders,
    }
    return render(request, "user/order_list.html", context)


class OrderDetail(DetailView):
  model = Order
  template_name = "user/order_detail.html"

  def dispatch(self, request, *args, **kwargs):
    try:
      user_check_id = self.request.session.get("user_checkout_id")
      user_checkout = UserCheckout.objects.get(id=user_check_id)
    except UserCheckout.DoesNotExist:
      user_checkout = UserCheckout.objects.get(user=request.user)
    except:
      user_checkout = None

    obj = self.get_object()
    if obj.user == user_checkout and user_checkout is not None:
      return super(OrderDetail, self).dispatch(request, *args, **kwargs)
    else:
      raise Http404