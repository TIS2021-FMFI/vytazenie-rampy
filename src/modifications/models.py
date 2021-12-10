from django.db import models

# Create your models here.
class TransportModification(models.Model):
    transport = models.ForeignKey("transports.Transport", models.PROTECT)
    user = models.ForeignKey(
        "accounts.CustomUser", models.PROTECT, verbose_name="Používateľ"
    )
    changes = models.JSONField(verbose_name="Zmeny")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Zmena prepráv'
        verbose_name_plural = 'Zmeny prepráv'
