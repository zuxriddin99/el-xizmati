from django.contrib import admin

from apps.users.models import User, UserAction


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "first_name", "last_name", "language"]
    search_fields = ["id", "phone_number", "first_name", "last_name", "language"]
    list_filter = ["language"]
    list_display_links = ["id", "phone_number"]


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ["id", "action_type", "phone_number", "code"]
    list_filter = ["action_type"]
