from django.forms.models import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from .forms import ProductCreateForm, ProductImageForm
from .models import Product, Category, ProductImage
from seller.models import SellerAccount

import random

# Create your views here.

class ProductDetailView(DetailView):
  model = Product

  def get_context_data(self, *args, **kwargs):
    context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
    
    # get related products by category
    instance = self.get_object()
    context["related"] = sorted(self.model.objects.get_related(instance)[:6], 
      key=lambda x: random.random())
        # context["related"] = Product.objects.get_related(instance).order_by("?")[:6]
    
    return context


class ProductListView(ListView):
  model = Product

  def get_context_data(self, **kwargs):
    context = super(ProductListView, self).get_context_data(**kwargs)
    context['category_list'] = Category.objects.all()
    return context 


class ProductCreateView(CreateView):
  model = Product
  template_name = "products/product_create.html"
  fields = '__all__'


  def get_context_data(self, *args, **kwargs):
    context = super(ProductCreateView, self).get_context_data(*args, **kwargs)
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=1)
    product_create_form = ProductCreateForm()
    product_image_formset = ImageFormSet(queryset=ProductImage.objects.none())
    context["product_create_form"] = product_create_form
    context["product_image_formset"] = product_image_formset
    return context

  def post(self, request, *args, **kwargs):
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=1)
    product_create_form = ProductCreateForm(request.POST)
    product_image_formset = ImageFormSet(request.POST, request.FILES,
                                          queryset=ProductImage.objects.none())

    if product_create_form.is_valid() and product_image_formset.is_valid():
      product_obj = product_create_form.save(commit=False) 
      seller = get_object_or_404(SellerAccount, user=self.request.user)
      product_obj.seller = seller 
      product_obj.save()

      for image_form in product_image_formset.cleaned_data:
        image = image_form['image']
        product_image = ProductImage(product=product_obj, image=image)
        product_image.save()

      return redirect("products:products")

    else:
      print (product_create_form.errors, product_image_formset.errors)




