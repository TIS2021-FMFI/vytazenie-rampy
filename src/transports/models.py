from django.db import models
from model_utils import FieldTracker
from django.shortcuts import render
from django.http import HttpRequest

# Create your models here.
class Transport(models.Model):
    registration_number = models.CharField("Evidenčné číslo vozidla", max_length=30)
    driver_name = models.CharField("Meno šoféra", max_length=50)
    carrier = models.ForeignKey(
        "Supplier", on_delete=models.CASCADE, verbose_name="Dodávateľ"
    )
    process_start = models.DateTimeField("Začiatok spracovania")
    process_finish = models.DateTimeField("Koniec spracovania")
    load = models.BooleanField("Nakládka")
    unload = models.BooleanField("Vykládka")
    transport_priority = models.ForeignKey("TransportPriority", models.CASCADE)
    transport_status = models.ForeignKey("TransportStatus", models.CASCADE)
    gate = models.ForeignKey("Gate", models.CASCADE, null=True, blank=True)
    canceled = models.BooleanField("Zrušená", default=False)
    created = models.DateTimeField("Vytvorený", auto_now_add=True)
    modified = models.DateTimeField("Upravený", auto_now=True)

    tracker = FieldTracker()

    def get_form(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST.id = self.id
        return render(request, "transports/form.html")


class Gate(models.Model):
    name = models.CharField("Brána", max_length=20)


class Supplier(models.Model):
    name = models.CharField("Názov", max_length=100)


class TransportPriority(models.Model):
    name = models.CharField("Názov", max_length=50)
    color = models.CharField("Farba", max_length=20)
    sort = models.PositiveSmallIntegerField("Poradie")
    is_default = models.BooleanField(default=False)


class TransportStatus(models.Model):
    name = models.CharField("Názov", max_length=30)
    color = models.CharField("Farba", max_length=20)
    is_default = models.BooleanField(default=False)
