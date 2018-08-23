from django.forms.models import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import View
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormMixin, CreateView, UpdateView
from django.views.generic.list import ListView


from billing.models import Transaction
from products.models import Product, Category, ProductImage, Tag
from products.forms import ProductForm, ProductImageForm, BaseProductImageFormSet

from .forms import NewSellerForm
from .mixins import SellerAccountMixin
from .models import SellerAccount


class SellerProductListView(SellerAccountMixin, FormMixin, View):
  def get(self, request, *args, **kwargs):
    context = {}
    context["products"] = self.get_products().order_by('-timestamp')
    context["seller"] = self.get_account()
    return render(request, "seller/product_list.html", context)



class SellerProductDetailRedirectView(RedirectView):
    permanent = True
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Product, slug=kwargs['slug'])
        return obj.get_absolute_url()


class ProductCreateView(SellerAccountMixin, CreateView):
  model = Product
  template_name = "seller/product_create.html"
  fields = '__all__'

  def get_context_data(self, *args, **kwargs):
    context = super(ProductCreateView, self).get_context_data(*args, **kwargs)
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=1)
    product_create_form = ProductForm()
    product_image_formset = ImageFormSet(queryset=ProductImage.objects.none())
    tags = Tag.objects.all()
    context["product_create_form"] = product_create_form
    context["product_image_formset"] = product_image_formset
    context["tags"] = tags
    return context

  def post(self, request, *args, **kwargs):
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=1)
    product_create_form = ProductForm(request.POST)
    product_image_formset = ImageFormSet(request.POST, request.FILES,
                                          queryset=ProductImage.objects.none())
    if product_create_form.is_valid() and product_image_formset.is_valid():
      product_obj = product_create_form.save(commit=False) 
      seller = get_object_or_404(SellerAccount, user=self.request.user)
      product_obj.seller = seller 
      tags = product_create_form.cleaned_data.get('tags')
      for tag in tags:
        Tag.objects.get_or_create(name=tag)
      product_obj.save()
      product_create_form.save_m2m()

      for image_form in product_image_formset:
        if image_form.instance.image:
          image = image_form.cleaned_data.get('image')
          product_image = ProductImage(product=product_obj, image=image)
          product_image.save()


      return redirect("products:products")

    else:
      print (product_create_form.errors, product_image_formset.errors)


# Modal product 
def save_product_form(request, form, image_form, template_name):
    data = dict()
    if request.method == 'POST':
        global dktp_list_display
        if form.is_valid() and image_form.is_valid():
            product_obj = form.save(commit=False)
            seller = get_object_or_404(SellerAccount, user=request.user)
            product_obj.seller = seller 
            tags = form.cleaned_data.get('tags')
            for tag in tags:
              tag_obj, created = Tag.objects.get_or_create(name=tag)
            product_obj.save()
            form.save_m2m()

            image_obj = image_form.cleaned_data.get("image")
            if image_obj:
              if image_form.instance.id == None:
                # Create new
                image = image_form.cleaned_data.get("image")
                product_image = ProductImage(product=product_obj, image=image)
                product_image.save()
              else:
                # Update old
                image_form.save()

            data['form_is_valid'] = True
            if dktp_list_display=='table':
              template = 'seller/partial_product_list.html'
              list_selector = '#dktp-seller-product-list tbody'
            else:
              template = 'seller/mb_partial_product_list.html'
              list_selector = '#mb-seller-product-list'
            products = Product.objects.all()

            data['html_product_list'] = render_to_string(template, {
                'products': products.order_by('-timestamp')
            })
            data['list_selector'] = list_selector
        else:
            data['form_is_valid'] = False

    dktp_list_display = request.GET.get('dktp_list_display', None)
    context = {
                'form': form,
                'image_form': image_form,
                }
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)



def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        image_form = ProductImageForm(request.POST, request.FILES)
    else:
        form = ProductForm()
        image_form = ProductImageForm()
    return save_product_form(request, form, image_form, 'seller/partial_product_create.html')


def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_image = product.productimage_set.first()
    if request.method == 'POST':
      form = ProductForm(request.POST, instance=product)
      image_form = ProductImageForm(request.POST, request.FILES, instance=product_image)
    else:
        form = ProductForm(instance=product)
        image_form = ProductImageForm(instance=product_image)
    return save_product_form(request, form, image_form, 'seller/partial_product_update.html')


def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    data = dict()
    if request.method == 'POST':
        global dktp_list_display
        product.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        products = Product.objects.all()
        if dktp_list_display=='table':
          template = 'seller/partial_product_list.html'
          list_selector = '#dktp-seller-product-list tbody'
        else:
          template = 'seller/mb_partial_product_list.html'
          list_selector = '#mb-seller-product-list'
        data['html_product_list'] = render_to_string(template, {
            'products': products.order_by('-timestamp')
        })
        data['list_selector'] = list_selector
    else:
        dktp_list_display = request.GET.get('dktp_list_display', None)
        context = {'product': product}
        data['html_form'] = render_to_string('seller/partial_product_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

class ProductUpdateView(SellerAccountMixin, UpdateView):
  model = Product
  template_name = "seller/product_update.html"
  fields = '__all__'

  def get_context_data(self, *args, **kwargs):
    context = super(ProductUpdateView, self).get_context_data(*args, **kwargs)
    product_edit_form = ProductForm(instance=self.get_product())
    hasImage = self.get_img_queryset().exists()
    if hasImage:
      ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, formset=BaseProductImageFormSet, extra=0, can_delete=True)
    else:
      ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, formset=BaseProductImageFormSet, extra=1, can_delete=True)
    product_image_formset = ImageFormSet(queryset=self.get_img_queryset())
    image_set = self.get_img_queryset()
    context["product_edit_form"] = product_edit_form
    context["product_image_formset"] = product_image_formset
    context["image_set"] = image_set
    return context
  
  def get_product(self, *args, **kwargs):
    product_slug = self.kwargs.get("slug")
    if product_slug:
      product = get_object_or_404(Product, slug=product_slug)
    return product

  def get_img_queryset(self, *args, **kwargs):
    product_slug = self.kwargs.get("slug")
    if product_slug:
      product = get_object_or_404(Product, slug=product_slug)
      queryset = ProductImage.objects.filter(product=product)
    return queryset

  def post(self, request, *args, **kwargs):
    product_edit_form = ProductForm(request.POST, instance=self.get_product())
    ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, formset=BaseProductImageFormSet, extra=0, can_delete=True)
    product_image_formset = ImageFormSet(request.POST, request.FILES, queryset=self.get_img_queryset())

    if product_edit_form.is_valid() and product_image_formset.is_valid():
      product_obj = product_edit_form.save(commit=False) 
      seller = get_object_or_404(SellerAccount, user=self.request.user)
      product_obj.seller = seller 

      tags = product_edit_form.cleaned_data.get('tags')
      for tag in tags:
        Tag.objects.get_or_create(name=tag)

      product_obj.save()
      product_edit_form.save_m2m()

      for image_form in product_image_formset:
        # Ignore empty input
        if image_form.instance.image:
          # Create new
          # Delete new is handled by jQuery dynamically on client side
          if image_form.instance.id == None:
            image = image_form.cleaned_data.get("image")
            product_image = ProductImage(product=product_obj, image=image)
            product_image.save()
          else:
            # Delete old
            if image_form.cleaned_data["DELETE"]:
              product_img = image_form.instance
              product_img.delete()
            # Update old
            else:
              image_form.save()

    else:
      print (product_edit_form.errors, product_image_formset.errors)

    return redirect("products:products")


class SellerTransactionListView(SellerAccountMixin, ListView):
  model = Transaction
  template_name = "seller/transaction_list_view.html"

  def get_queryset(self):
    return self.get_transactions()



class SellerDashboard(SellerAccountMixin, FormMixin, View):
  form_class = NewSellerForm
  success_url = "/seller/"

  def post(self, request, *args, **kwargs):
    form = self.get_form()
    if form.is_valid():
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

  def get(self, request, *args, **kwargs):
    apply_form = self.get_form() #NewSellerForm()
    account = self.get_account()
    exists = account
    active = None
    context = {}
    if exists:
      active = account.active
    if not exists and not active:
      context["title"] = "Apply for Account"
      context["apply_form"] = apply_form
    elif exists and not active:
      context["title"] = "Account Pending"
    elif exists and active:
      context["title"] = "Seller Dashboard"
      
      #products = Product.objects.filter(seller=account)
      context["products"] = self.get_products()[:5]
      transactions_today = self.get_transactions_today()
      context["transactions_today"] = transactions_today
      context["transactions"] = self.get_transactions().exclude(pk__in=transactions_today)[:5]
      context["today_sales"] = self.get_today_sales()
      context["total_sales"] = self.get_total_sales()

    else:
      pass
    
    return render(request, "seller/dashboard.html", context)

  def form_valid(self, form):
    valid_data = super(SellerDashboard, self).form_valid(form)
    obj = SellerAccount.objects.create(user=self.request.user)
    return valid_data