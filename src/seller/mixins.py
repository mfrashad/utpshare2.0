import datetime
import pytz

from django.db.models import Count, Min, Sum, Avg, Max

from utpshare.mixins import LoginRequiredMixin
from products.models import Product
from sales.models import Sale

from .models import SellerAccount


class SellerAccountMixin(LoginRequiredMixin):
  account = None
  products = []
  sales = []

  def get_account(self):
    user = self.request.user
    accounts = SellerAccount.objects.filter(user=user)
    if accounts.exists() and accounts.count() == 1:
      self.account = accounts.first()
      return accounts.first()
    return None

  def get_products(self):
    account = self.get_account()
    products = Product.objects.filter(seller=account)
    self.products = products
    return products

  def get_sales(self):
    account = self.get_account()
    sales = Sale.objects.filter(seller=account).order_by('-timestamp')
    self.sales = sales
    return sales

  def get_sales_today(self):
    today = datetime.date.today()
    today_min_naive = datetime.datetime.combine(today, datetime.time.min)
    today_max_naive = datetime.datetime.combine(today, datetime.time.max)
    timezone = pytz.timezone("Asia/Kuala_Lumpur")
    today_min_aware = timezone.localize(today_min_naive)
    today_max_aware = timezone.localize(today_max_naive)
    return self.get_sales().filter(timestamp__range=(today_min_aware, today_max_aware))

  def get_sales_recent(self):
    sales_today = self.get_sales_today()
    return self.get_sales().exclude(pk__in=sales_today)[:5]

  def get_total_sales(self):
    sales = self.get_sales()
    total_sales = 0
    for sale in sales:
      total_sales += sale.compute_sale_total()
    return total_sales

  def get_total_sales_today(self):
    sales = self.get_sales_today()
    total_sales = 0
    for sale in sales:
      total_sales += sale.compute_sale_total()
    return total_sales

  def get_total_sales_recent(self):
    sales = self.get_sales_recent()
    total_sales = 0
    for sale in sales:
      total_sales += sale.compute_sale_total()
    return total_sales