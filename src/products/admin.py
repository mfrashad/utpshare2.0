from django.contrib import admin
from .models import Product, ProductImage, Category

# Register your models here.
class ProductImageInline(admin.TabularInline):
  model = ProductImage 
  extra = 0
  max_num = 10

class ProductAdmin(admin.ModelAdmin):
  list_display = ["__str__", "seller", "description", "price"]
  list_filter = ["price"]
  inlines = [ProductImageInline,]
  class Meta:
    model = Product 

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Category)