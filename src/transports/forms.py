from django.forms import ModelForm, HiddenInput

from .models import Transport


class TransportForm(ModelForm):
    class Meta:
        model = Transport
        widgets = {"id": HiddenInput()}
        exclude = ["created", "modified"]
