from django import forms
from .models import  Product, ProductImage

class ProductCreateForm(forms.ModelForm):
  class Meta:
    model = Product 
    fields = [
            "title",
            "category",
            "price",
            "description",
            "stock_count",
    ]

class ProductImageForm(forms.ModelForm):
  class Meta:
    model = ProductImage
    fields = [
            'image',
    ]


