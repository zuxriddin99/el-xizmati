from django.contrib import admin

from apps.main.models import Region, District


# Register your models here.
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


# Register your models here.
@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "region"]
    list_filter = ["region"]
    search_fields = ["name"]
