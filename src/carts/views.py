from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin

# Create your views here.

from orders.forms import GuestCheckoutForm
from orders.mixins import CartOrderMixin
from orders.models import Order, UserAddress

from products.models import Product
from carts.models import Cart, CartItem

from sales.models import Sale

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
  template_name = "carts/cart.html"

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
    delete_order = request.GET.get("delete_order", False)
    add_item = False
    if item_slug:
      item = get_object_or_404(Product, slug=item_slug)
      seller = item.seller 
      qty = request.GET.get("qty", 1)
      cart_item, add_item = CartItem.objects.get_or_create(cart=cart, item=item, seller=seller)
      if delete_item:
        cart_item.delete()
        if cart.items.count() == 0:
          try:
            order=Order.objects.get(cart=cart)
            order.delete()
            del request.session["order_id"]
          except:
            pass
          cart.delete()
          del request.session["cart_id"]
      else:
        cart_item.quantity = qty
        cart_item.save()

      if not request.is_ajax():
        return HttpResponseRedirect(reverse("cart"))

    if delete_order:
      order=Order.objects.get(cart=cart)
      order.delete()
      del request.session["order_id"]
      cart.delete()
      del request.session["cart_id"]
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


class CheckoutView(CartOrderMixin, FormMixin, View):
  model = Cart
  template_name = "carts/checkout_view.html"

  def get(self, request, *args, **kwargs):
    context = {}
    user_can_continue = False
    order = self.get_order()
    if self.request.user.is_authenticated():
      user_can_continue = True
      user_address = UserAddress.objects.get_or_create(user=self.request.user)[0]
      if user_address.address == None:
        return redirect("user_address_create")
      order.user = self.request.user
      order.user_address = user_address
      order.save()
    else:
      context["login_form"] = AuthenticationForm()
      context["registration_form"] = RegistrationForm()
      context["next_url"] = self.request.build_absolute_uri()

    context["order"] = order
    context["user_can_continue"] = user_can_continue

    template = self.template_name
    return render(request, template, context)

  def get_success_url(self):
    return reverse("checkout")



class CheckoutFinalView(CartOrderMixin, View):
  def post(self, request, *args, **kwargs):
    order = self.get_order()

    seller_list = []
    for cartitem in order.cart.cartitem_set.all():
      seller = cartitem.item.seller
      if seller not in seller_list:
        seller_list.append(seller)

    for seller in seller_list:
      # cart_item = order.cart.cartitem_set.filter(seller=seller)
      # print(cart_item)
      sale = Sale.objects.create(seller=seller)
      sale.order.add(order)

    if request.POST.get("payment_token") == "ABC":
      order.status = "completed"
      order.save()
      del request.session["cart_id"]
      del request.session["order_id"]
    return redirect("user:order_detail", pk=order.pk)


  # def get(self, request, *args, **kwargs):
  #   return redirect("checkout")