from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms 
from django.forms import ModelForm, widgets
# from django.forms.formsets import BaseFormSet
from django.forms.models import BaseModelFormSet
from .models import  Product, ProductImage

from .models import ProductImage


class ProductForm(ModelForm):
  class Meta:
    model = Product 
    fields = [
            "title",
            "stock_count",
            "price",
            "category",
            "description",
            "tags",
    ]

  def __init__(self, *args, **kwargs):
    super(ProductForm, self).__init__(*args, **kwargs)
    self.fields['tags'].widget.attrs.update({
        'class': 'tag-field-css-hard-fix',
    })

  # def __init__(self, *args, **kwargs):
  #   super(ProductForm, self).__init__(*args, **kwargs)
  #   self.helper = FormHelper()
  #   self.helper.form_tag = False
  #   self.helper.layout = Layout(
  #       Div(
  #           Div('title', css_class="col-sm-12"),
  #           css_class = 'row'
  #       ),
  #       Div(
  #           Div('price', css_class="col-sm-6"),
  #           Div('category', css_class="col-sm-6"),
  #           css_class = 'row'
  #       ),
  #       Div(
  #           Div('stock_count', css_class="col-sm-12"),
  #           css_class = 'row'
  #       ),
  #       Div(
  #           Div('description', css_class="col-sm-12"),
  #           css_class = 'row'
  #       ),
  #       Div(
  #           Div('tags', css_class="col-sm-12"),
  #           css_class = 'row'
  #       ),
  #   )


# copied from django/forms/widgets.py
class FileInput(widgets.Input):
    input_type = 'file'
    needs_multipart_form = True

    def render(self, name, value, attrs=None):
        return super(FileInput, self).render(name, None, attrs=attrs)

    def value_from_datadict(self, data, files, name):
        "File widgets take data from FILES, not POST"
        return files.get(name)


# class CustomClearableFileInput(widgets.ClearableFileInput):
#     # only works with django>=1.11
#     template_name = 'custom_clearable_file_input.html'


class ProductImageForm(ModelForm):
  class Meta:
    model = ProductImage
    fields = ['image']
    widgets = {'image': FileInput}

  def __init__(self, *args, **kwargs):
    super(ProductImageForm, self).__init__(*args, **kwargs)
    self.fields['image'].label = ""


class BaseProductImageFormSet(BaseModelFormSet):
  def add_fields(self, form, index):
    super(BaseProductImageFormSet, self).add_fields(form, index)
    if self.can_delete:
        form.fields['DELETE'].widget = forms.HiddenInput()



