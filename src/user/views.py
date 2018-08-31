import random

from django.views.generic import View
from django.shortcuts import render

# Create your views here.

from products.models import Product

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
