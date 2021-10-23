from django import forms
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    UserCreationForm,
    UserChangeForm,
    UsernameField,
)
from .models import CustomUser

from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")
        field_classes = {"username": UsernameField}


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Skutočné heslá nie sú uložené v databáze. Jediný spôsob ako zistiť heslo "
            "tohto používateľa, je ho zmeniť cez "
            '<a href="{}">tento formulár</a>.'
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email")
