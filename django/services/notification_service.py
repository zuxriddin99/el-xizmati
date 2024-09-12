from apps.users.models import User, UserNotification


class NotificationService:

    def user_notifications(self, user: User):
        return UserNotification.objects.filter(user=user)