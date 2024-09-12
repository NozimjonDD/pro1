from django.conf import settings

from django.contrib.auth.models import AbstractUser, Group as AbstractGroup
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django.db import models
from apps.common.models import BaseModel
from . import utils
from apps.common import utils as common_utils
from ..common.data import UserRoleChoices


class User(AbstractUser, BaseModel):
    phone_number = models.CharField(
        verbose_name=_("phone number"),
        unique=True,
        error_messages={
            "unique": _("A user with that phone number already exists."),
        },
        max_length=100,
        validators=[common_utils.phone_number_validator]
    )
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        null=True,
        blank=True
    )
    role = models.CharField(choices=UserRoleChoices.choices, default=UserRoleChoices.USER, max_length=50)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    middle_name = models.CharField(_("middle name"), max_length=150, blank=True)

    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    profile_picture = models.ImageField(
        verbose_name=_("profile picture"),
        upload_to="profile_pictures/",
        null=True,
        blank=True,
    )

    balance = models.DecimalField(verbose_name=_("Balance"), max_digits=18, decimal_places=2, default=100000000)
    coin_balance = models.DecimalField(verbose_name=_("Coin balance"), max_digits=18, decimal_places=2, default="0.00")

    EMAIL_FIELD = None
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "user"
        ordering = ["-date_joined"]
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.phone_number

    def generate_otp(self):
        otp = self.user_otps.filter(
            is_deleted=False,
            is_confirmed=False,
            created_at__gt=timezone.now() - timezone.timedelta(seconds=settings.OTP_EXPIRATION_TIME)
        ).first()

        if otp:
            return otp

        otp = UserOTP.objects.create(user=self, code=utils.generate_otp())
        return otp

    @property
    def p_team(self):
        if hasattr(self, "team"):
            return self.team
        return None

    @property
    def account_settings(self):
        if hasattr(self, "_account_settings"):
            return self._account_settings
        return AccountSettings.objects.create(user_id=self.pk)

    @property
    def pretty_balance(self):
        return common_utils.pretty_price(self.balance)

    def generate_refresh_token(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        from rest_framework_simplejwt.settings import api_settings
        from django.contrib.auth.models import update_last_login

        refresh = RefreshToken.for_user(self)
        data = dict()
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self)

        return data

    def delete_account(self):
        """
        change user phone number to: deleted__+998901234567__timestamp
        :return: None
        """
        self.is_active = False
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.phone_number = f"deleted__{self.phone_number}__{timezone.now().timestamp()}"
        self.save()


class AccountSettings(BaseModel):
    class Meta:
        db_table = "account_settings"
        verbose_name = _("Account settings")
        verbose_name_plural = _("Account settings")

    class LangChoices(models.TextChoices):
        UZ = "uz", _("O'zbekcha")
        RU = "ru", _("Русский")

    user = models.OneToOneField(
        to="User", on_delete=models.CASCADE, related_name="_account_settings", verbose_name=_("user")
    )
    lang = models.CharField(
        verbose_name=_("language"),
        max_length=2,
        choices=LangChoices.choices,
        default=LangChoices.UZ
    )
    push_notifications = models.BooleanField(
        verbose_name=_("push notifications"),
        default=True
    )

    def __str__(self):
        return f"{self.user} - account settings"


class Device(BaseModel):
    class Meta:
        db_table = "user_device"
        verbose_name = _("User device")
        verbose_name_plural = _("User devices")

    user = models.ForeignKey(
        to="users.User", on_delete=models.CASCADE, verbose_name=_("User"), related_name="devices"
    )
    device_id = models.CharField(verbose_name=_("Device ID"), max_length=255, null=True, unique=True)
    fcm_token = models.CharField(verbose_name=_("FCM token"), max_length=255, unique=True)
    name = models.CharField(verbose_name=_("Device name"), max_length=255)
    device_type = models.CharField(verbose_name=_("Device type"), max_length=20)

    def __str__(self):
        return f"{self.user} - {self.name}"


class GroupProxyModel(AbstractGroup):
    class Meta:
        proxy = True
        verbose_name = _("group")
        verbose_name_plural = _("groups")
        ordering = ["name"]


class UserOTP(BaseModel):
    class Meta:
        db_table = "user_otp"
        verbose_name = _("user OTP")
        verbose_name_plural = _("user OTPs")

    user = models.ForeignKey(
        to="User", on_delete=models.CASCADE, related_name="user_otps", verbose_name=_("user")
    )
    code = models.CharField(verbose_name=_("code"), max_length=10)
    secret = models.CharField(verbose_name=_("secret"), max_length=50, unique=True, default=utils.generate_secret)
    is_confirmed = models.BooleanField(verbose_name=_("is confirmed"), default=False)

    def __str__(self):
        return str(self.created_at)

    def is_expired(self):
        if self.is_confirmed or self.is_deleted:
            return True
        if timezone.now() - self.created_at > timezone.timedelta(seconds=settings.OTP_EXPIRATION_TIME):
            return True
        return False
