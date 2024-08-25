from django.contrib import admin

from apps.ads.models import Category, AD, ADMedia


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name_uz", "order"]


class ADMediaInline(admin.TabularInline):
    model = ADMedia
    extra = 0


@admin.register(AD)
class ADAdmin(admin.ModelAdmin):
    list_display = ["id", "owner", "name"]
    inlines = [ADMediaInline]
