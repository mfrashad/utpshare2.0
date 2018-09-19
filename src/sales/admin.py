from django.contrib import admin
from .models import Sale

# Register your models here.

class SaleAdmin(admin.ModelAdmin):
  list_display = ["__str__", "seller", "order", "timestamp"]
  class Meta:
    model = Sale

admin.site.register(Sale, SaleAdmin)
