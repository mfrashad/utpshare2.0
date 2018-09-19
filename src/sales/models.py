from django.db import models
from carts.models import CartItem
from seller.models import SellerAccount
from orders.models import Order
# Create your models here.

SALE_STATUS_CHOICES = (
  ('pending', 'Pending'),
  ('approved', 'Approved'),
  ('delivered', 'Delivered'),
)

class Sale(models.Model):
  seller = models.ForeignKey(SellerAccount, on_delete=models.CASCADE)
  timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  status = models.CharField(max_length=120, choices=SALE_STATUS_CHOICES, default='pending')

  def __str__(self):
    return str(self.id)

  def get_seller_item_list(self):
    seller = self.seller
    seller_item_list = self.order.cart.cartitem_set.filter(seller=seller)
    return seller_item_list

  def compute_sale_total(self):
    seller_item_list = self.get_seller_item_list()
    sale_total = 0
    for seller_item in seller_item_list:
      sale_total += seller_item.line_total
    return sale_total
