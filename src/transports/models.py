from typing import Union
from datetime import datetime
from django.core.exceptions import ValidationError

from django.db import models
from model_utils import FieldTracker
from dateutil import parser


class Transport(models.Model):
    LOAD_COLOR = "#0099D4"
    UNLOAD_COLOR = "#EE9800"
    BOTH_COLOR = "#7B67A8"

    registration_number = models.CharField("Evidenčné číslo vozidla", max_length=30)
    driver_name = models.CharField("Meno šoféra", max_length=50)
    supplier = models.ForeignKey(
        "Supplier", on_delete=models.CASCADE, verbose_name="Dodávateľ"
    )
    carrier = models.ForeignKey(
        "Carrier", on_delete=models.CASCADE, verbose_name="Prepravca"
    )
    process_start = models.DateTimeField("Začiatok spracovania")
    process_finish = models.DateTimeField("Koniec spracovania")
    load = models.BooleanField("Nakládka")
    unload = models.BooleanField("Vykládka")
    transport_priority = models.ForeignKey("TransportPriority", models.CASCADE)
    transport_status = models.ForeignKey("TransportStatus", models.CASCADE)
    gate = models.ForeignKey("Gate", models.CASCADE, null=True, blank=True)
    canceled = models.BooleanField("Zrušená", default=False)
    note = models.CharField(
        "Poznámka", blank=True, null=False, default="", max_length=100
    )
    created = models.DateTimeField("Vytvorený", auto_now_add=True)
    modified = models.DateTimeField("Upravený", auto_now=True)

    tracker = FieldTracker()

    class Meta:
        verbose_name_plural = "Prepravy"
        verbose_name = "Preprava"
        indexes = [
            models.Index(fields=['process_start'])
        ]

    @staticmethod
    def find_objects_between_timestamps(
        start: Union[str, datetime], end: Union[str, datetime]
    ):
        """
        Finds transports between specified datetimes.
        """
        if isinstance(start, str) and isinstance(end, str):
            start = parser.parse(start)
            end = parser.parse(end)

        return Transport.objects.filter(
            process_start__range=(start, end)
        )

    def __str__(self):
        start, end = self._format_datetime(self.process_start), self._format_datetime(
            self.process_finish
        )
        return (
            "Preprava EČV " + self.registration_number + " od " + start + " do " + end
        )

    def _format_datetime(self, datetime):
        """
        Utility function to format datetime.
        """
        return datetime.strftime("%d. %m. %Y %H:%M")

    @property
    def color(self):
        """
        Returns background color of the transport according to load/unload flags set on the object.
        Used by API serializer.
        """
        return (
            self.BOTH_COLOR
            if self.load and self.unload
            else (self.LOAD_COLOR if self.load else self.UNLOAD_COLOR)
        )

    def clean(self):
        """
        Custom Transport validation which takes in mind business logic.
        """

        # TODO: implementovat vsetky obmedzenia na tvorbu preprav (2 prepravy v rovnakom case na jednej brane atd.)
        if self.process_finish <= self.process_start:
            raise ValidationError(
                {
                    "process_finish": "Spracovanie prepravy musí skončiť neskôr ako jej začiatok."
                }
            )


class Gate(models.Model):
    name = models.CharField("Názov", max_length=20)

    class Meta:
        verbose_name_plural = "Brány"
        verbose_name = "Brána"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField("Názov", max_length=100)

    class Meta:
        verbose_name_plural = "Dodávatelia"
        verbose_name = "Dodávateľ"

    def __str__(self):
        return self.name


class Carrier(models.Model):
    name = models.CharField("Názov", max_length=100)

    class Meta:
        verbose_name_plural = "Dopravcovia"
        verbose_name = "Dopravca"

    def __str__(self):
        return self.name


class TransportPriority(models.Model):
    name = models.CharField("Názov", max_length=50)
    color = models.CharField("Farba", max_length=20)
    font_color = models.CharField("Farba textu", max_length=20, default="#000000")
    sort = models.PositiveSmallIntegerField("Poradie")
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Priority prepráv"
        verbose_name = "Priorita prepráv"

    def __str__(self):
        return self.name


class TransportStatus(models.Model):
    name = models.CharField("Názov", max_length=30)
    color = models.CharField("Farba", max_length=20)
    font_color = models.CharField("Farba textu", max_length=20, default="#000000")
    sort = models.PositiveSmallIntegerField("Poradie")
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Stavy prepráv"
        verbose_name = "Stav prepráv"

    def __str__(self):
        return self.name
