from django.forms import ModelForm

from .models import Transport


class TransportForm(ModelForm):
    class Meta:
        model = Transport
        exclude = ["created", "modified"]
