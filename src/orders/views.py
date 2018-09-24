from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
# Create your views here.

from .forms import UserAddressForm
from .mixins import CartOrderMixin, LoginRequiredMixin
from .models import UserAddress, UserCheckout, Order



class UserAddressCreateView(CartOrderMixin, CreateView):
  model = UserAddress
  template_name = "orders/user_address_create.html"
  fields = '__all__'

  def get_checkout_user(self):
      user_check_id = self.request.session.get("user_checkout_id")
      user_checkout = UserCheckout.objects.get(id=user_check_id)
      return user_checkout

  def get_context_data(self, *args, **kwargs):
    context = super(UserAddressCreateView, self).get_context_data(*args, **kwargs)
    form = UserAddressForm()
    context["form"] = form
    return context

  def post(self, request, *args, **kwargs):
    form = UserAddressForm(request.POST)
    if form.is_valid():
      print("3")
      user = self.get_checkout_user()
      address = form.cleaned_data["address"]
      user_address = UserAddress.objects.get(user=user)
      user_address.address = address
      user_address.save()
      order = self.get_order()
      order.user_address = user_address
      order.save()
      return redirect("checkout")
    else:
      print (form.errors)




# class UserAddressCreateView(CartOrderMixin, CreateView):
#   form_class = UserAddressForm
#   template_name = "forms.html"
#   success_url = "/checkout/"

#   def get_checkout_user(self):
#     user_check_id = self.request.session.get("user_checkout_id")
#     user_checkout = UserCheckout.objects.get(id=user_check_id)
#     return user_checkout

#   def form_valid(self, form, *args, **kwargs):
#     print("success")
#     user = self.get_checkout_user()
#     address = form.cleaned_data["address"]
#     form.instance.user = user
#     form.instance.address = address
#     # order = self.get_order()

#     # order.save()
#     return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)


