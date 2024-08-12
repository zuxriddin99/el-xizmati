from django.contrib import admin

from apps.ads.models import Category


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "order"]
