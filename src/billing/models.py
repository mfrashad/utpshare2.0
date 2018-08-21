from django.conf import settings
from django.db import models

# Create your models here.

from products.models import Product

class Transaction(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
  timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
  success = models.BooleanField(default=True)

  def __unicode__(self):
    return "%s" %(self.id)
