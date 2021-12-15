from django import forms
from .models import Transport

default_attrs = {
    forms.Select: {"class": "form-select", "autocomplete": False},
    forms.NullBooleanSelect: {"class": "form-select", "autocomplete": False},
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
