from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from seller.models import SellerAccount

# Create your models here.

class ProductManager(models.Manager):
  def get_related(self, instance):
    products = self.get_queryset().filter(category = instance.category).exclude(id=instance.id)
    return products

class Product(models.Model):
  seller = models.ForeignKey(SellerAccount, on_delete=models.CASCADE)
  title = models.CharField(max_length=50)
  slug = models.SlugField(blank=True, unique=True)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
  sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
  stock_count = models.PositiveSmallIntegerField(default=1)
  category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.CASCADE)

  objects = ProductManager()

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse("products:product_detail", kwargs={"slug": self.slug})

  def get_image_url(self):
    img = self.productimage_set.first()
    if img:
      return img.image.url
    return img  #None

  def get_html_price(self):
    if self.sale_price is not None:
      html_text = "<span class='sale-price'>%s</span>&emsp;<span class='og-price small'>%s</span>"\
        %(self.sale_price, self.price)
    else:
      html_text = "<span class='price'>%s</span>" %(self.price)
    return mark_safe(html_text) 

def create_slug(instance, new_slug=None):
  # 1st time coming in
  slug = slugify(instance.title)
  # 2nd time coming in
  if new_slug is not None:
    slug = new_slug

  # To check if this slug is unique
  # if slug exists, create a new slug by appending its id to it
  qs = Product.objects.filter(slug=slug)
  exists = qs.exists()
  if exists:
    # qs.first().id is used coz instance not saved yet and instance.id not created
    new_slug = "%s-%s" %(slug, qs.first().id)
    # return a fx so that the loop repeats itself again
    return create_slug(instance, new_slug=new_slug)

  return slug 

def product_pre_save_receiver(sender, instance, *args, **kwargs):
  if not instance.slug:
    instance.slug = create_slug(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)


# Product Images
def image_upload_to(instance, filename):
  title = instance.product.title
  slug = slugify(title)
  basename, file_extension = filename.split(".")
  new_filename = "%s.%s" %(slug, file_extension)
  return "products/%s/%s" %(slug, new_filename)


class ProductImage(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  image = models.ImageField(upload_to=image_upload_to)

  def __str__(self):
    return self.product.title


class Category(models.Model):
  title = models.CharField(max_length=50, unique=True)
  slug = models.SlugField(blank=True, unique=True)

  def __str__(self):
    return self.title

def category_pre_save_receiver(sender, instance, *args, **kwargs):
  if not instance.slug:
    instance.slug = slugify(instance.title)

pre_save.connect(category_pre_save_receiver, sender=Category)
