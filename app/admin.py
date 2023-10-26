from django.contrib import admin
from django import forms
from django.utils.html import format_html

from .models import *


# Register your models here.
class CriminalImageInline(admin.TabularInline):
    model = CriminalImage
    extra = 1  # Specify the number of empty forms to display


class CriminalAdminForm(forms.ModelForm):
    class Meta:
        model = Criminal
        fields = '__all__'
        widgets = {
            'Criminal_Description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


@admin.register(Criminal)
class CriminalAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'Criminal_Description')
    list_filter = ('Criminal_Firstname', 'Criminal_Lastname')
    search_fields = ('Criminal_Firstname', 'Criminal_Lastname')
    inlines = [CriminalImageInline]  # Include the inline for CriminalImages
    form = CriminalAdminForm


@admin.register(CriminalImage)
class CriminalImageAdmin(admin.ModelAdmin):
    list_display = ('Criminal', 'image_thumbnail')
    list_filter = ('Criminal__Criminal_Firstname', 'Criminal__Criminal_Lastname')
    search_fields = ('Criminal__Criminal_Firstname', 'Criminal__Criminal_Lastname')

    def image_thumbnail(self, obj):
        if obj.Criminal_Image:
            thumbnail_url = obj.Criminal_Image.url  # Assuming this is the URL of the thumbnail
            return format_html('<a href="{}" target="_blank"><img src="{}" width="50" height="50" /></a>',
                               obj.Criminal_Image.url, thumbnail_url)
        return 'No Image'

    image_thumbnail.short_description = 'Criminal Image'
