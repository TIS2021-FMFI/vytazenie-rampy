from django.contrib import admin
from .models import Supplier, Transport, TransportPriority, TransportStatus, Gate

# Register your models here.
models = (Supplier, Transport, TransportPriority, TransportStatus, Gate)
admin.site.register(models)
