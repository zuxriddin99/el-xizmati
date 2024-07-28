from django.db import models

from django.contrib.auth.models import AbstractUser, Permission
from django.utils.translation import gettext_lazy as _

from apps.base_app.models import BaseModel
from apps.users.managers import CustomUserManager
from apps.users.validator import validate_uzbekistan_phone


# Create your models here.
class LanguageEnum(models.TextChoices):
    UZ = 'uz', _('Uzbek')
    RU = 'ru', _('Russian')
    EN = 'en', _('English')


class UserRoleEnum(models.TextChoices):
    WORKER = "worker", _('Worker')
    EMPLOYER = "employer", _('Employer')


class User(AbstractUser, BaseModel):
    phone_number = models.CharField(
        max_length=20, unique=True, verbose_name="Phone Number", validators=[validate_uzbekistan_phone])
    language = models.CharField(max_length=2, choices=LanguageEnum.choices, default=LanguageEnum.UZ, blank=True)
    photo = models.ImageField(upload_to="user_photos/", null=True, blank=True)
    pasport_serial_number = models.CharField(blank=True, null=True, max_length=20)
    role = models.CharField(choices=UserRoleEnum.choices, default=UserRoleEnum.EMPLOYER, max_length=10)
    username = None
    groups = None
    user_permissions = None
    email = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)


class UserAction(BaseModel):
    class ActionTypeEnum(models.TextChoices):
        LOGIN = "login"

    action_type = models.CharField(choices=ActionTypeEnum.choices, default=ActionTypeEnum.LOGIN, max_length=20)
    phone_number = models.CharField(
        max_length=20, unique=True, verbose_name="Phone Number", validators=[validate_uzbekistan_phone])
    code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.phone_number} | {self.code} "
