from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils.translation import gettext_lazy as _

from . forms import CustomUserChangeForm, CustomUserCreationForm
from . models import Timezone, User

class Group(DjangoGroup):
    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'
        proxy = True

class GroupAdmin(BaseGroupAdmin):
    pass

class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]

    list_display_links = ["email", "username"]
    list_filter = [
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]
    fieldsets = (
        (
            _("Login Credentials"),
            {"fields": ("email", "password")},
        ),
        (
            _("Personal Information"),
            {"fields": ("username", "first_name", "last_name", "timezone", "avatar")},
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important Dates"),
            {"fields": ("date_joined", "last_login")},
        ),
    )

    add_fieldsets = (
        None,
        {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        },
    )

    search_fields = ["email", "username", "first_name", "last_name"]


class TimezoneAdmin(admin.ModelAdmin):
    list_display = ["name", "timestamp"]
    list_filter = ["name", "timestamp"]

    fieldsets = (
        (
            _('Details'),
            {"fields": ("name", "timestamp")}
        ),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Timezone, TimezoneAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.unregister(DjangoGroup)