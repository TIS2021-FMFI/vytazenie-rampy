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
    CachedModel,
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
                self.fields[field].widget.attrs = dict(
                    default_attrs[self.fields[field].widget.__class__]
                )
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

    def __init__(self, user, *args, **kwargs):
        super(TransportForm, self).__init__(*args, **kwargs)

        editable_fields = ()
        for field in self.fields:
            if user.has_perm(f"transports.edit_detailfield_{field}"):
                editable_fields += (field,)

        self.readonly_fields = tuple(
            field for field in self.fields if field not in editable_fields
        )

        # ! in case of an emergency use the below code instead
        # self.readonly_fields = ()
        # user_group = str(user.groups.first().custom_group)
        # if user_group == "Transport manažment":
        #     self.readonly_fields = ("gate", "transport_status")
        # elif user_group == "Predák":
        #     self.readonly_fields = tuple(field for field in self.fields if field not in ("gate"))
        # elif user_group == "Skladník":
        #     self.readonly_fields = tuple(field for field in self.fields if field not in ("transport_status"))

        self.apply_restrictions()

        for field in fk_fields:
            self.fields[field].choices = self._get_model_choices(fk_fields[field])
            if not self.fields[field].required:
                self.fields[field].choices.insert(0, ("", "------"))

    def is_valid(self):
        is_valid = super(TransportForm, self).is_valid()

        if not is_valid:
            for field in self.fields:
                if not self.errors.get(field):
                    continue

                self.fields[field].widget.attrs["class"] += " is-invalid"
        return is_valid

    def _get_model_choices(self, model):
        cache_key = CachedModel.get_model_choices_cache_key(model)
        choices = cache.get_or_set(
            cache_key,
            [(choice.pk, str(choice)) for choice in model.objects.all()],
            self.MODEL_CHOICES_CACHE_DURATION,
        )
        return choices

    def apply_restrictions(self):
        for field in self.readonly_fields:
            self.fields[field].required = False
            self.fields[field].widget.attrs["disabled"] = "disabled"
