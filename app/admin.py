from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Book)


class CriminalImageAdmin(admin.StackedInline):
    model = CriminalImage


@admin.register(Criminal)
class CriminalAdmin(admin.ModelAdmin):
    inlines = [CriminalImageAdmin]


@admin.register(CriminalImage)
class CriminalImageAdmin(admin.ModelAdmin):
    pass
