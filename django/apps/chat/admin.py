from django.contrib import admin

from apps.chat.models import Chat, Message, MessageMedia


# Register your models here.

class MessageInline(admin.StackedInline):
    model = Message
    extra = 1


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ["id", "count_unread_messages"]
    inlines = [MessageInline]
