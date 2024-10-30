import random

from rest_framework import exceptions
from rest_framework.exceptions import ParseError, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User, UserAction


class AuthService:

    def send_sms_to_phone(self, **kwargs):
        phone_number = kwargs.get('phone_number')
        # code = self.generate_code()
        code = "0000"
        user, _ = UserAction.objects.update_or_create(phone_number=phone_number, defaults={'code': code})
        # todo need to add smm sender function

    @staticmethod
    def generate_code():
        return ''.join(random.choices('0123456789', k=4))

    def verify_phone_number(self, **kwargs):
        phone_number = kwargs.get('phone_number')
        code = kwargs.get('code')
        try:
            UserAction.objects.get(phone_number=phone_number)
        except UserAction.DoesNotExist:
            raise exceptions.NotFound(detail='For the number not sent sms before that use auth/send-sms/ endpoint',
                                      code="WRONG_CODE")

        try:
            UserAction.objects.get(phone_number=phone_number, code=code)
        except UserAction.DoesNotExist:
            raise exceptions.NotFound(detail='Wrong code', code="WRONG_CODE")

        user, is_created = User.objects.get_or_create(phone_number=phone_number)
        return {
            "phone_number": phone_number,
            "is_created": is_created,
            "tokens": self.get_user_tokens(user)
        }

    @staticmethod
    def get_user_tokens(user: User) -> dict:
        """Получение токена"""
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    @staticmethod
    def set_user_info(user: User, **kwargs):
        if user.is_anonymous:
            raise exceptions.NotFound(detail='User does not exist', code="USER_DOES_NOT_EXIST")
        for key, value in kwargs.items():
            setattr(user, key, value)

        user.save()
        return user


class UserService:
    @staticmethod
    def update_user_role(user: User, role: str):
        user.role = role
        user.save()
