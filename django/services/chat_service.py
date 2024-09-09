from apps.chat.models import Chat, Message, MessageMedia
from apps.users.models import User


class ChatService:

    @staticmethod
    def chats_list(request_user: User):
        return Chat.objects.filter(users=request_user)


class MessageService:

    @staticmethod
    def create_message(user: User, **val_data):
        medias = val_data.pop("medias", [])
        msg = Message.objects.create(author=user, **val_data)
        for i in medias:
            media_type = i.content_type.split("/")[0]
            MessageMedia.objects.create(message=msg, media_type=media_type, file=i)
        return msg

    @staticmethod
    def get_messages(chat_id: int):
        return Message.objects.filter(chat_id=chat_id).order_by("-created_at")
