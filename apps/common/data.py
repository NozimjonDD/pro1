from django.db import models
from django.utils.translation import gettext_lazy as _


class LeagueStatusType(models.TextChoices):
    PUBLIC = 'public', 'Public',
    PRIVATE = 'private', 'Private',


class LeagueStatusChoices(models.TextChoices):
    PENDING = "pending", _("Pending")
    ACTIVE = "active", _("Active")
    INACTIVE = "inactive", _("Inactive")
    SUSPENDED = "suspended", _("Suspended")


class LeagueParticipantStatusChoices(models.TextChoices):
    ACTIVE = "active", _("Active")
    SUSPENDED = "suspended", _("Suspended")


class TeamStatusChoices(models.TextChoices):
    ACTIVE = 'active', 'Active',
    INACTIVE = 'inactive', 'Inactive',
    DRAFT = "draft", "Draft"


class UserRoleChoices(models.TextChoices):
    USER = 'user', 'User',
    ADMIN = 'admin', 'Admin',
    MODERATOR = 'moderator', 'Moderator',


class TransferTypeChoices(models.TextChoices):
    SELL = "sell", _("Sell")
    BUY = "buy", _("Buy")
    SWAP = "swap", _("Swap")


class TariffTypeChoices(models.TextChoices):
    FREE = 'free', _("Free")
    STANDARD = 'standard', _("Standard")
    ADVANCED = "advanced", _("Advanced")
