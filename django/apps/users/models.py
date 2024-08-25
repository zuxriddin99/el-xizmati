from apps.base_app.models import BaseModel
from apps.main.models import District
from apps.users.managers import CustomUserManager
from apps.users.validator import validate_uzbekistan_phone
from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class LanguageEnum(models.TextChoices):
    UZ = 'uz', _('Uzbek')
    RU = 'ru', _('Russian')
    EN = 'en', _('English')
    OZ = 'oz', _('Uzbek kyril')


class UserRoleEnum(models.TextChoices):
    WORKER = "worker", _('Worker')
    EMPLOYER = "employer", _('Employer')


class User(AbstractUser, BaseModel):
    phone_number = models.CharField(
        max_length=20, unique=True, verbose_name="Phone Number", validators=[validate_uzbekistan_phone])
    language = models.CharField(max_length=2, choices=LanguageEnum.choices, default=LanguageEnum.UZ, blank=True)
    photo = models.ImageField(upload_to="user_photos/", null=True, blank=True)
    passport_serial_number = models.CharField(blank=True, null=True, max_length=20)
    role = models.CharField(choices=UserRoleEnum.choices, default=UserRoleEnum.EMPLOYER, max_length=10)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, blank=True)

    username = None
    groups = None
    user_permissions = None
    email = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)

    @property
    def quantity_ads(self):
        return self.owner_ads.all().count()

    @property
    def rating(self):
        # need count rating
        return 5


class UserAction(BaseModel):
    class ActionTypeEnum(models.TextChoices):
        LOGIN = "login"

    action_type = models.CharField(choices=ActionTypeEnum.choices, default=ActionTypeEnum.LOGIN, max_length=20)
    phone_number = models.CharField(
        max_length=20, unique=True, verbose_name="Phone Number", validators=[validate_uzbekistan_phone])
    code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.phone_number} | {self.code} "


class NotificationTypeEnum(models.TextChoices):
    NEW_MSG = "new_msg", _('New Message')
    OFFER_ACCEPT = "offer_accept", _('Offer Accepted')
    OFFER_REJECT = "offer_reject", _('Offer Rejected')
    INFO = "info", _('Info')


def user_notif_image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/ad_<id>/<filename>
    return f"user_{instance.ad.owner_id}/notifications/notif_{instance.id}/{filename}"


class UserNotification(BaseModel):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    notif_type = models.CharField(
        choices=NotificationTypeEnum.choices, max_length=20, default=NotificationTypeEnum.INFO)
    title = models.CharField(max_length=250)
    description = models.TextField(default="")
    image = models.ImageField(upload_to=user_notif_image_directory_path, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("User Notification")
        verbose_name_plural = _("User Notifications")
        db_table = "user_notifications"
