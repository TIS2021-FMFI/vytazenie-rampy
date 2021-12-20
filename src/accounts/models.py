from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
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
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_("Vyplňuje sa automaticky pri zadaní krstného mena a priezviska."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return (
            self.first_name + " " + self.last_name
            if self.first_name and self.last_name
            else self.username
        )


class View(models.Model):
    class ViewEnum(models.TextChoices):
        WEEK = "week", _("Týždeň")
        DEN = "day", _("Deň")
        TABULKA = "table", _("Tabuľka")

    class Meta:
        verbose_name = "Pohľad"
        verbose_name_plural = "Pohľady"

    name = models.CharField("názov", max_length=30)
    view = models.CharField(
        max_length=10, choices=ViewEnum.choices, null=False, blank=False
    )

    def __str__(self):
        return self.name


class CustomGroup(models.Model):
    group = models.OneToOneField(
        Group, models.CASCADE, verbose_name="Skupina", related_name="custom_group"
    )
    allowed_views = models.ManyToManyField(
        View, verbose_name="Povolený pohľad", related_name="allowed_views"
    )
    default_view = models.ForeignKey(
        View, models.CASCADE, verbose_name="Východzí pohľad"
    )

    def __str__(self):
        return self.group.name

    class Meta:
        verbose_name = "Rozšírené možnosti skupiny"
        verbose_name_plural = "Rozšírené možnosti skupiny"

    def save(self, *args, **kwargs):
        if self.pk:
            if self.allowed_views.all().count() == 0:
                raise ValidationError("Skupina musí mať aspoň jeden povolený pohľad!")
            if self.allowed_views.filter(pk=self.default_view_id).count() == 0:
                raise ValidationError(
                    "Východzí pohľad sa musí nachádzať v povolených pohľadoch!"
                )

        return super(CustomGroup, self).save(*args, **kwargs)
