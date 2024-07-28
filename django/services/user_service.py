import random

from apps.users.models import User, UserAction


class AuthService:

    def send_sms_to_phone(self, phone_number: str):
        code = self.generate_code()
        user, _ = UserAction.objects.update_or_create(phone_number=phone_number, defaults={'code': code})
        # todo need to add smm sender function

    @staticmethod
    def generate_code():
        return ''.join(random.choices('0123456789', k=4))


