import logging
from django import forms
from django.core.cache import cache
from .models import (
    Transport,
    TransportPriority,
    TransportStatus,
    Gate,
    Supplier,
    Carrier,
    get_model_choices_cache_key,
)

logger = logging.getLogger(__file__)

default_attrs = {
    forms.Select: {"class": "form-select", "autocomplete": False},
    forms.NullBooleanSelect: {"class": "form-select", "autocomplete": False},
    forms.CheckboxInput: {"class": "form-check-input", "role": "switch"},
}

fk_fields = {
    "transport_priority": TransportPriority,
    "transport_status": TransportStatus,
    "gate": Gate,
    "supplier": Supplier,
    "carrier": Carrier,
}


class DefaultBootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DefaultBootstrapForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            try:
                self.fields[field].widget.attrs = default_attrs[
                    self.fields[field].widget.__class__
                ]
            except KeyError:
                self.fields[field].widget.attrs = {"class": "form-control"}


class TransportForm(DefaultBootstrapForm):
    MODEL_CHOICES_CACHE_DURATION = 600

    process_start = forms.DateTimeField(
        widget=forms.widgets.DateTimeInput(format="%d.%m.%Y %H:%M:%S")
    )
    process_finish = forms.DateTimeField(
        widget=forms.widgets.DateTimeInput(format="%d.%m.%Y %H:%M:%S")
    )

    class Meta:
        model = Transport
        exclude = ["created", "modified"]

    def __init__(self, *args, **kwargs):
        super(TransportForm, self).__init__(*args, **kwargs)

        for field in fk_fields:
            self.fields[field].choices = self._get_model_choices(fk_fields[field])

        for field in self.fields:
            if self.fields[field].required:
                try:
                    self.fields[field].empty_label = None
                except AttributeError:
                    pass

    def is_valid(self):
        is_valid = super(TransportForm, self).is_valid()

        if not is_valid:
            for field in self.fields:
                if not self.errors.get(field):
                    continue

                self.fields[field].widget.attrs["class"] += " is-invalid"
        return is_valid

    def _get_model_choices(self, model):
        cache_key = get_model_choices_cache_key(model)
        choices = cache.get_or_set(
            cache_key,
            [(choice.pk, str(choice)) for choice in model.objects.all()],
            self.MODEL_CHOICES_CACHE_DURATION,
        )
        return choices
