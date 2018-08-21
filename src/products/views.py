from django.db.models import Q
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Product, Category, ProductImage, Tag
from analytics.models import TagView
import random

# Create your views here.

class TagListView(ListView):
  model = Tag

  def get_context_data(self, *args, **kwargs):
    context = super(TagListView, self).get_context_data(*args, **kwargs)
    context["tag_list"] = self.get_queryset().order_by('-count', '?')
    return context

class TagDetailView(DetailView):
  model = Tag

  def get_context_data(self, *args, **kwargs):
    context = super(TagDetailView, self).get_context_data(*args, **kwargs)
    tag_slug = self.kwargs.get("slug")
    tag = Tag.objects.filter(slug=tag_slug)
    tag_products = Product.objects.filter(tags=tag)
    context["tag_products"] = tag_products
    return context


class ProductDetailView(DetailView):
  model = Product

  def get_context_data(self, *args, **kwargs):
    context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
    
    # get related products by category
    instance = self.get_object()
    tags = instance.tags.all()
    context["related"] = sorted(self.model.objects.get_related(instance)[:6], 
      key=lambda x: random.random())

    if self.request.user.is_authenticated():
      for tag in tags:
        TagView.objects.add_count(self.request.user, tag)
    return context


class ProductListView(ListView):
  model = Product

  def get_context_data(self, **kwargs):
    context = super(ProductListView, self).get_context_data(**kwargs)
    context['category_list'] = Category.objects.all()
    return context 


class ProductSearchListView(ListView):
  model = Product
  template_name = "products/product_search_list.html"

  def get_queryset(self, *args, **kwargs):
    qs = super(ProductSearchListView, self).get_queryset(**kwargs)
    query = self.request.GET.get("q")
    qs = qs.filter(
        Q(title__icontains=query)|
        Q(description__icontains=query)
      ).order_by("-timestamp")
    return qs 

  def get_context_data(self, *args, **kwargs):
    context = super(ProductSearchListView, self).get_context_data(*args, **kwargs)
    count = self.get_queryset().count()
    if count<1:
      context["title"] = "No results found."
    elif count==1:
      context["title"] = "%s %s" %(count, "result found.")
    else:
      context["title"] = "%s %s" %(count, "results found.")
    
    return context












