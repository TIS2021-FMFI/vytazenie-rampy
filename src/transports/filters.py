from django_filters import FilterSet, BooleanFilter
from django.forms import widgets
from .models import Transport
from .forms import DefaultBootstrapForm

filter_fields = {
    'process_start': ['lt', 'gt'],
    'transport_status': ['exact'],
    'transport_priority': ['exact'],
    'gate': ['exact'],
    'load': ['exact'],
    'unload': ['exact'],
    'supplier': ['exact'],
    'carrier': ['exact'],
    'canceled': ['exact'],
    'driver_name': ['icontains'],
    'registration_number': ['icontains'],
}


class TransportFilterForm(DefaultBootstrapForm):
    class Meta:
        model = Transport
        fields = filter_fields.keys()


boolean_choices = [
    (None, 'Všetko'),
    (True, 'Áno'),
    (False, 'Nie'),
]


class TransportFilter(FilterSet):
    load = BooleanFilter(widget=widgets.Select(choices=boolean_choices))
    unload = BooleanFilter(widget=widgets.Select(choices=boolean_choices))
    canceled = BooleanFilter(widget=widgets.Select(choices=boolean_choices))

    class Meta:
        model = Transport
        fields = filter_fields
        form = TransportFilterForm

