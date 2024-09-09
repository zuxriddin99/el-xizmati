from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.base_app.models import BaseModel


# Create your models here.

class ChatBase(BaseModel):
    class Meta:
        abstract = True
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")

class MessageBase(BaseModel):
    text = models.TextField(blank=True, default="")
    was_read = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        abstract = True
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


class Chat(ChatBase):
    users = models.ManyToManyField("users.User", related_name="chats")
    count_unread_messages = models.IntegerField(default=0)
    last_message = models.ForeignKey(
        "chat.Message", related_name="+", null=True, blank=True, on_delete=models.SET_NULL)

    def get_partner(self, request_user_id: int):
        return self.users.exclude(id=request_user_id).first()

    class Meta:
        db_table = "chats"

class Message(MessageBase):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey("users.User", related_name="user_messages", on_delete=models.CASCADE)
    ad = models.ForeignKey("ads.AD", related_name="messages", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "messages"

def message_media_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/ad_<id>/<filename>
    return f"user_{instance.message.author_id}/messages/message_{instance.message_id}/{filename}"

class MessageMediaTypeEnum(models.TextChoices):
    IMAGE = "image", _("Image")
    VIDEO = "video", _("Video")


class MessageMedia(BaseModel):
    message = models.ForeignKey(Message, related_name="medias", on_delete=models.CASCADE)
    file = models.FileField(upload_to=message_media_directory_path)
    media_type = models.CharField(
        max_length=6, choices=MessageMediaTypeEnum.choices, default=MessageMediaTypeEnum.IMAGE)

    class Meta:
        db_table = "message_medias"
        verbose_name = "Message Media"
        verbose_name_plural = "Message Medias"


class TechSupportChat(ChatBase):
    owner = models.OneToOneField("users.User", related_name="tech_support", on_delete=models.CASCADE)
    telegram_group_id = models.CharField(max_length=255, null=True, blank=True)
    has_unread_message = models.BooleanField(default=False)

    class Meta:
        db_table = "tech_support_chats"
        verbose_name = _("Tech Support Chat")
        verbose_name_plural = _("Tech Support Chats")


class TechSupportMessage(MessageBase):
    chat = models.ForeignKey(TechSupportChat, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey("users.User", related_name="user_tech_support_messages", on_delete=models.CASCADE)

    class Meta:
        db_table = "tech_support_messages"
        verbose_name = _("Tech Support Message")
        verbose_name_plural = _("Tech Support Messages")

def tech_support_message_media_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/ad_<id>/<filename>
    return f"user_{instance.message.author_id}/tech_support/message_{instance.message_id}/{filename}"

class TechSupportMessageMedia(BaseModel):
    message = models.ForeignKey(TechSupportMessage, related_name="medias", on_delete=models.CASCADE)
    file = models.FileField(upload_to=message_media_directory_path)
    media_type = models.CharField(
        max_length=6, choices=MessageMediaTypeEnum.choices, default=MessageMediaTypeEnum.IMAGE)

    class Meta:
        db_table = "tech_support_message_medias"
        verbose_name = "Message Media"
        verbose_name_plural = "Message Medias"


