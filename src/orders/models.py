from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
# Create your models here.
from carts.models import Cart

from .utils import unique_order_id_generator


class UserCheckout(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True) #not required
  email = models.EmailField(unique=True) #--> required


  def __str__(self): #def __str__(self):
    return self.email

  def get_checkout_user(self):
    if self.user:
      return self.user
    else:
      return self.email




class UserAddress(models.Model):
  user = models.OneToOneField(UserCheckout)
  address = models.CharField(max_length=120, null=True, blank=True)

  def __str__(self):
    return str(self.user.email)

  # def get_address(self):
  #   return self.address




class Order(models.Model):
  cart = models.ForeignKey(Cart)
  user = models.ForeignKey(UserCheckout, null=True)
  user_address = models.ForeignKey(UserAddress, null=True)
  order_total = models.DecimalField(max_digits=50, decimal_places=2)
  order_id= models.CharField(max_length=120, blank= True, default='')
  time_created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.order_id)


def order_pre_save(sender, instance, *args, **kwargs):
  cart_total = instance.cart.cart_total
  instance.order_total = cart_total

  if not instance.order_id:
    instance.order_id= unique_order_id_generator(instance)
    print(instance.order_id)

pre_save.connect(order_pre_save, sender=Order)