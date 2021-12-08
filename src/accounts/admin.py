from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, CustomGroup, View


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "first_name",
        "last_name",
        "email",
        "username",
    ]
    list_display_links = ("first_name", "last_name", "email", "username")

    prepopulated_fields = {"username": ("first_name", "last_name")}

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "username",
                    "password1",
                    "password2",
                ),
            },
        ),
        (_('Permissions'), {
            'fields': ('is_superuser', 'groups', 'user_permissions'),
        }),
    )

class CustomGroupInline(admin.StackedInline):
    model = CustomGroup

class NewGroupAdmin(GroupAdmin):
    inlines = GroupAdmin.inlines + [CustomGroupInline]

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.unregister(Group)
admin.site.register(Group, NewGroupAdmin)

admin.site.register(View)
