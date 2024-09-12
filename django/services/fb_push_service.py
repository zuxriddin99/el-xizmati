from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

from apps.users.models import User


class FirebasePushService:

    @staticmethod
    def send_push(user: User, data: dict, title='', body=''):
        devices = FCMDevice.objects.filter(user=user)
        for i in devices:
            i.send_message(Message(data=data, notification=Notification(
                title=str(title),
                body=str(body),
            )
            ))

    def send_push_new_message(self, user: User, chat_id: int, text=""):
        title = f"{user.first_name} {user.last_name}"
        body = text if text else "New Message"
        data = {"chat_id": chat_id}
        self.send_push(user=user, data=data, title=title, body=body)