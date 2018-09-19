from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete

from products.models import Product
from seller.models import SellerAccount

# Create your models here.

class CartItem(models.Model):
  seller = models.ForeignKey(SellerAccount)
  cart = models.ForeignKey("Cart")
  item = models.ForeignKey(Product)
  quantity = models.PositiveIntegerField(default=1)
  line_total = models.DecimalField(max_digits=10, decimal_places=2)

  def __str__(self):
    return self.item.title

  def remove(self):
    return self.item.remove_from_cart()


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
  qty = instance.quantity
  if int(qty) >= 1:
    price = instance.item.price
    line_total = Decimal(qty) * Decimal(price)
    instance.line_total = line_total

pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
  instance.cart.update_subtotal()

post_save.connect(cart_item_post_save_receiver, sender=CartItem)

post_delete.connect(cart_item_post_save_receiver, sender=CartItem)


class Cart(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
  items = models.ManyToManyField(Product, through=CartItem)
  time_created = models.DateTimeField(auto_now_add=True, auto_now=False)
  time_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
  subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
  delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  cart_total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
  # discount
  # negotiation_price

  def __str__(self):
    return str(self.id)

  def update_subtotal(self):
    subtotal = 0
    items = self.cartitem_set.all()
    for item in items:
      subtotal += item.line_total
    self.subtotal = "%.2f" %(subtotal)
    self.save()


def get_cart_total_receiver(sender, instance, *args, **kwargs):
  subtotal = Decimal(instance.subtotal)
  # delivery_fee = round(subtotal * Decimal(0.085), 2) #8.5%
  delivery_fee = round(Decimal(1.20), 2)
  cart_total = round(subtotal + Decimal(delivery_fee), 2)
  instance.delivery_fee = "%.2f" %(delivery_fee)
  instance.cart_total = "%.2f" %(cart_total)
  #instance.save()


pre_save.connect(get_cart_total_receiver, sender=Cart)