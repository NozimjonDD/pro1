from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin, GroupAdmin as DjangoGroupAdmin
from django.utils.translation import gettext_lazy as _

from django.utils.html import format_html

from users import models

admin.site.unregister(Group)


@admin.register(models.GroupProxyModel)
class GroupAdmin(DjangoGroupAdmin):
    pass


class AccountSettingsInline(admin.StackedInline):
    model = models.AccountSettings
    can_delete = False
    verbose_name_plural = "Account settings"
    fk_name = "user"
    fields = ("lang", "push_notifications",)


@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "phone_number", "username", "profile_pic_html", "first_name",
        "last_name", "middle_name", "is_active", "is_staff", "is_superuser", "date_joined", "id",
    )
    list_display_links = ("phone_number",)
    fieldsets = (
        (None, {"fields": ("phone_number", "username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "middle_name", "profile_picture", "date_of_birth")}
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_number", "username", "password1", "password2"),
            },
        ),
    )
    ordering = ("-date_joined",)
    inlines = (AccountSettingsInline,)

    def profile_pic_html(self, obj):
        if obj.profile_picture:
            return format_html(f'<img src="{obj.profile_picture.url}" width="50" height="50";">')

    profile_pic_html.short_description = _("Profile picture")
