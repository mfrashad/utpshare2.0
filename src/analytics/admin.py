from django.contrib import admin

# Register your models here.

from .models import TagView


class TagViewAdmin(admin.ModelAdmin):
    list_display = ["__str__", "count", "user"]
    class Meta:
      model = TagView


admin.site.register(TagView, TagViewAdmin)