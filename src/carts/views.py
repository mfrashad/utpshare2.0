from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin

# Create your views here.

from orders.forms import GuestCheckoutForm
from orders.mixins import CartOrderMixin
from orders.models import UserCheckout, Order, UserAddress

from products.models import Product
from carts.models import Cart, CartItem

class ItemCountView(View):
  def get(self, request, *args, **kwargs):
    if request.is_ajax():
      cart_id = self.request.session.get("cart_id")
      if cart_id == None:
        count = 0
      else:
        cart = Cart.objects.get(id=cart_id)
        count = cart.items.count()

      request.session["cart_item_count"] = count
      return JsonResponse({"count": count})
    else:
      raise Http404


class CartView(SingleObjectMixin, View):
  model = Cart
  template_name = "carts/view.html"

  def get_or_create_cart(self, *args, **kwargs):
    self.request.session.set_expiry(0)
    cart_id = self.request.session.get("cart_id")
    if cart_id == None:
      cart = Cart()
      cart.save()
      cart_id = cart.id  
      self.request.session["cart_id"] = cart_id
    cart = Cart.objects.get(id=cart_id)
    if self.request.user.is_authenticated():
      cart.user = self.request.user
      cart.save()
    return cart

  def get(self, request, *args, **kwargs):
    cart = self.get_or_create_cart()
    item_slug = request.GET.get("item_slug")
    delete_item = request.GET.get("delete_item", False)
    add_item = False
    if item_slug:
      item = get_object_or_404(Product, slug=item_slug)
      qty = request.GET.get("qty", 1)
      cart_item, add_item = CartItem.objects.get_or_create(cart=cart, item=item)
      if delete_item:
        cart_item.delete()
      else:
        cart_item.quantity = qty
        cart_item.save()

      if not request.is_ajax():
        return HttpResponseRedirect(reverse("cart"))

    if request.is_ajax():
      try:
        line_total = cart_item.line_total
      except:
        line_total = None
      try:
        subtotal = cart_item.cart.subtotal
      except:
        subtotal = None
      try:
        delivery_fee = cart_item.cart.delivery_fee
      except:
        delivery_fee = None
      try:
        cart_total = cart_item.cart.cart_total
      except:
        cart_total = None
      try:
        total_items = cart_item.cart.items.count()
      except:
        total_items = 0
      data = {
              "delete_item": delete_item,
              "add_item": add_item,
              "line_total": line_total,
              "subtotal": subtotal,
              "delivery_fee": delivery_fee,
              "cart_total": cart_total,
              "total_items": total_items,
      }
      return JsonResponse(data)
    
    context = {
      "cart": cart
    }
    template = self.template_name
    return render(request, template, context)
    # return HttpResponseRedirect("/products/")


# class CheckoutView(DetailView):
#   model = Cart
#   template_name = "carts/checkout_view.html"

#   def get_object(self, *args, **kwargs):
#     cart_id = self.request.session.get("cart_id")
#     if cart_id == None:
#       return redirect("cart")
#     cart = Cart.objects.get(id=cart_id)
#     return cart

#   def get_context_data(self, *args, **kwargs):
#     context = super(CheckoutView, self).get_context_data(*args, **kwargs)
#     user_can_continue = False
#     if not self.request.user.is_authenticated():# or if request.user.is_guest:
#       context["login_form"] = AuthenticationForm()
#       context["next_url"] = self.request.build_absolute_uri()
#     if self.request.user.is_authenticated(): #or if request.user.is_guest():
#       user_can_continue = True
#     context["user_can_continue"] = user_can_continue
#     return context


class CheckoutView(CartOrderMixin, FormMixin, DetailView):
  model = Cart
  template_name = "carts/checkout_view.html"
  form_class = GuestCheckoutForm

  def get_object(self, *args, **kwargs):
    cart = self.get_cart()
    if cart == None:
      return None
    return cart

  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    form = self.get_form()
    if form.is_valid():
      email = form.cleaned_data.get("email")
      user_checkout, created = UserCheckout.objects.get_or_create(email=email)
      print(user_checkout)
      request.session["user_checkout_id"] = user_checkout.id
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

  def get_context_data(self, *args, **kwargs):
    context = super(CheckoutView, self).get_context_data(*args, **kwargs)
    print("1")
    user_can_continue = False
    user_checkout_id = self.request.session.get("user_checkout_id")
    if self.request.user.is_authenticated():
      user_can_continue = True
      user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
      user_checkout.user = self.request.user
      user_checkout.save()
      self.request.session["user_checkout_id"] = user_checkout.id
    elif not self.request.user.is_authenticated() and user_checkout_id == None:
      context["login_form"] = AuthenticationForm()
      context["next_url"] = self.request.build_absolute_uri()
    else:
      pass
    user_checkout_id = self.request.session.get("user_checkout_id")
    order = self.get_order()
    if user_checkout_id != None:
      user_can_continue = True
      user_checkout = UserCheckout.objects.get(id=user_checkout_id)
      user_address = UserAddress.objects.get_or_create(user=user_checkout)[0]
      order.user_address = user_address
      order.save()
    context["order"] = order
    context["user_can_continue"] = user_can_continue
    context["form"] = self.get_form()
    return context

  def get_success_url(self):
    return reverse("checkout")


  def get(self, request, *args, **kwargs):
    get_data  = super(CheckoutView, self).get(request, *args, **kwargs)
    print("2")
    cart = self.get_object()
    if cart == None:
      return redirect("cart")
    new_order = self.get_order()
    user_checkout_id = self.request.session.get("user_checkout_id")
    if user_checkout_id != None:
      user_checkout = UserCheckout.objects.get(id=user_checkout_id)
      user_address = UserAddress.objects.get_or_create(user=user_checkout)[0]
      if user_address.address == None:
        return redirect("user_address_create")
      new_order.user = user_checkout
      new_order.user_address = user_address
      new_order.save()
    return get_data




class CheckoutFinalView(CartOrderMixin, View):
  def post(self, request, *args, **kwargs):
    order = self.get_order()
    if request.POST.get("payment_token") == "ABC":
      order.mark_completed()
      messages.success(request, "Thank you for your order.")
      del request.session["cart_id"]
      del request.session["order_id"]
    return redirect("order_detail", pk=order.pk)

  def get(self, request, *args, **kwargs):
    return redirect("checkout")