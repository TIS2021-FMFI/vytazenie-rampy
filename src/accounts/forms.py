from django import forms
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    UserCreationForm,
    UserChangeForm,
    UsernameField,
)
from .models import CustomUser

from django.utils.translation import gettext_lazy as _

help_text = """
<ul>
    <li>Vaše heslo nemôže byť príliš podobné ostatným údajom, ktoré ste vo formulári vyplnili.</li>
    <li>Vaše heslo musí obsahovať aspoň 8 znakov.</li>
    <li>Vaše heslo nemôže byť bežne používané heslo.</li>
    <li>Vaše heslo nemôže obsahovať iba číslice.</li>
</ul>
"""


class CustomUserCreationForm(UserCreationForm):
    disabled_fields = ["username"]

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=help_text,
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email")
        field_classes = {"username": UsernameField, "email": forms.EmailField}

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field in self.disabled_fields:
            self.fields[field].widget.attrs["readonly"] = True


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
