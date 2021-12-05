from django.contrib import admin
from .models import Supplier, Transport, TransportPriority, TransportStatus, Gate, Carrier

# Register your models here.
models = (Supplier, Transport, TransportPriority, TransportStatus, Gate, Carrier)
admin.site.register(models)
