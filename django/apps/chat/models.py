from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.base_app.models import BaseModel


# Create your models here.

class Chat(BaseModel):
    users = models.ManyToManyField("users.User", related_name="chats")
    is_tech_support = models.BooleanField(default=False)
    telegram_group_id = models.CharField(max_length=255, null=True, blank=True)

    def get_partner(self, request_user_id: int):
        self.users.exclude(id=request_user_id)

    class Meta:
        db_table = "chats"
        verbose_name = "Chat"
        verbose_name_plural = "Chats"


class Message(BaseModel):
    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey("users.User", related_name="user_messages", on_delete=models.CASCADE)
    text = models.TextField()
    was_read = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        db_table = "messages"
        verbose_name = "Message"
        verbose_name_plural = "Messages"

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

