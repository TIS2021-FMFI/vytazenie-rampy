from django.contrib.auth.models import AbstractUser
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
    email = models.EmailField(_("email address"), blank=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    username_validator = EmailValidator()

    def __str__(self):
        return (
            self.first_name + " " + self.last_name
            if self.first_name and self.last_name
            else self.username
        )
