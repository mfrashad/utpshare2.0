from django.contrib import admin
from .models import Product, ProductImage, Category, Subcategory, Tag

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


class ProductImageAdmin(admin.ModelAdmin):
  list_display = ["id", "__str__"]
  class Meta:
    model = ProductImage

class SubcategoryAdmin(admin.ModelAdmin):
  list_display = ["__str__", "category"]
  list_filter = ["category"]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Category)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Tag)