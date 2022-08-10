from django.contrib import admin

from .models import Conversion, SilentList

# Register your models here.


class ConversionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "video_url")


admin.site.register(Conversion, ConversionAdmin)


class SilentListAdmin(admin.ModelAdmin):
    list_display = ("user_email", )


admin.site.register(SilentList, SilentListAdmin)
