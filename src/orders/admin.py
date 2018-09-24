from django.contrib import admin

# Register your models here.


from .models import UserCheckout, UserAddress, Order

class UserCheckoutAdmin(admin.ModelAdmin):
  list_display = ["id", "__str__"]
  class Meta:
    model = UserCheckout

class OrderAdmin(admin.ModelAdmin):
  list_display = ["id", "user", "__str__", "time_created"]
  class Meta:
    model = Order


admin.site.register(UserCheckout, UserCheckoutAdmin)
admin.site.register(UserAddress)
admin.site.register(Order, OrderAdmin)
