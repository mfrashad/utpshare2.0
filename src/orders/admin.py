from django.contrib import admin

# Register your models here.


from .models import UserAddress, Order


class OrderAdmin(admin.ModelAdmin):
  list_display = ["id", "user", "__str__", "time_created"]
  class Meta:
    model = Order

admin.site.register(UserAddress)
admin.site.register(Order, OrderAdmin)
