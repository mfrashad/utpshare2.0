from decimal import Decimal
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
# Create your models here.
from carts.models import Cart

class UserCheckout(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True) #not required
  email = models.EmailField(unique=True) #--> required


  def __str__(self): #def __str__(self):
    return self.email




class UserAddress(models.Model):
  user = models.OneToOneField(UserCheckout)
  address = models.CharField(max_length=120, null=True, blank=True)

  def __str__(self):
    return str(self.user.email)

  def get_address(self):
    return self.address


ORDER_STATUS_CHOICES = (
  ('created', 'Created'),
  ('completed', 'Completed'),
)


class Order(models.Model):
  status = models.CharField(max_length=120, choices=ORDER_STATUS_CHOICES, default='created')
  cart = models.ForeignKey(Cart)
  user = models.ForeignKey(UserCheckout, null=True)
  user_address = models.ForeignKey(UserAddress, null=True)
  order_total = models.DecimalField(max_digits=50, decimal_places=2)
  #order_id

  def __str__(self):
    return str(self.cart.id)

  def mark_completed(self):
    self.status = "completed"
    self.save()


def order_pre_save(sender, instance, *args, **kwargs):
  cart_total = instance.cart.cart_total
  instance.order_total = cart_total

pre_save.connect(order_pre_save, sender=Order)