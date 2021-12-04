from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class CustomUser(AbstractUser):
    is_superuser = models.BooleanField(
        _("administrátor"),
        default=False,
        help_text=_("Administrátor má automaticky všetky práva nastavené."),
    )

    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Vyplňuje sa automaticky pri zadaní krstného mena a priezviska.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return (
            self.first_name + " " + self.last_name
            if self.first_name and self.last_name
            else self.username
        )
