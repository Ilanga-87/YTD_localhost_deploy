from django.contrib import admin

from .models import Conversion

# Register your models here.


class ConversionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "video_url")


admin.site.register(Conversion, ConversionAdmin)
