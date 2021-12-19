import json
import pathlib
import csv
import logging
import time
from collections import OrderedDict
from dateutil import parser
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.cache import cache
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.generic.list import ListView
from openpyxl import Workbook
from .forms import TransportForm
from .filters import TransportFilter
from .utils import TransportChangeTracker
from .models import Transport, TransportPriority, TransportStatus
from modifications.models import TransportModification

logger = logging.getLogger(__file__)


@login_required
def view_based_on_user_group(request):
    return redirect(request.user.groups.first().custom_group.default_view.view)


@login_required
def form(request, pk=None):
    """
    Create new Transport and update existing one. Track changes made on Transports
    along with user who submitted them.
    """
    _form = None
    saved = False

    try:
        inst = Transport.objects.get(pk=pk)
    except Transport.DoesNotExist:
        inst = None

    if request.method == "POST":
        tracker = TransportChangeTracker(request.POST, inst, request.user)

        if tracker.is_valid():
            saved = True
            tracker.track()
            messages.add_message(
                request, messages.SUCCESS, "Preprava bola úspešne upravená."
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Prepravu sa nepodarilo upraviť. Skontrolujte prosím vyplnené údaje.",
            )

        _form = tracker.get_form()

    # get instance if primary key is provided
    if _form is None:
        _form = TransportForm(
            instance=inst, initial=_get_default_transport_data() if pk is None else {}
        )

    context = {"form": _form, "saved": saved}

    if request.user.is_superuser and request.method == "GET":
        # if user is administrator, include transport modifications in context
        changes = tuple(
            TransportModification.objects.filter(transport_id=pk)
            .order_by("created")
            .all()
        )

        # first fetch from cache, if not available, parse changes
        cache_key = 'transport_modifications_' + str(hash(changes))
        changes_cached = cache.get(cache_key)
        if changes_cached is not None:
            context.update(changes_cached)
        else:
            context['changes_parsed'] = []
            for change in changes:
                changes_dict = json.loads(change.changes)
                context["changes_parsed"].append({
                    "date": change.created,
                    "user": str(change.user),
                    "changes": _parse_transport_modification_changes(changes_dict)
                })

            context["latest_changes"] = _create_latest_changes(changes)
            cache.set(cache_key, {"latest_changes": context["latest_changes"], "changes_parsed": context["changes_parsed"]})

    return render(request, "transports/elements/form.html", context)

def _parse_transport_modification_changes(changes):
    changes_str = []
    for field in changes:
        field_name = Transport._meta.get_field(field).verbose_name
        changes_str.append(f'{field_name}: {_format_change_value(changes[field]["BEFORE"])} -> {_format_change_value(changes[field]["AFTER"])}')
    return changes_str

def _format_change_value(value):
    try:
        return Transport._format_datetime(parser.parse(value))
    except:
        if isinstance(value, bool):
            return 'áno' if value else 'nie'
        return value

def _create_latest_changes(changes):
    my_dict = {
        "process_start": None,
        "process_finish": None,
        "registration_number": None,
        "driver_name": None,
        "supplier": None,
        "carrier": None,
        "transport_priority": None,
        "transport_status": None,
        "gate": None,
        "note": None,
        "load": None,
        "unload": None,
        "canceled": None
    }
    for change in reversed(changes[1:]):
        changes_dict = json.loads(change.changes)
        for field in changes_dict:
            #check if field is string
            res = isinstance(field, str)
            if res:
                x = field.replace("_id","")
            else:
                x = field

            if my_dict[x] is not None:
                continue

            #check if before and after are strings
            if isinstance(changes_dict[field]["BEFORE"], str):
                before = changes_dict[field]["BEFORE"].replace("_id", "")
                after = changes_dict[field]["AFTER"].replace("_id", "")
            else:
                before = changes_dict[field]["BEFORE"]
                after = changes_dict[field]["AFTER"]

            my_dict[x] = f'{str(change.user)}: {_format_change_value(before)} -> {_format_change_value(after)}'

            if all([x is not None for x in my_dict.values()]):
                return my_dict

    return my_dict

@user_passes_test(
    lambda user: user.is_superuser
    or user.has_perm('accounts.weekly_view')
    or user.groups.first().custom_group.allowed_views.filter(view="week").exists(),
    None,
    "",
)
def week(request):
    context = {
        "title_appendix": "Týždenný pohľad",
        "calendar_controls": True,
        "color_helper" : {
            "load": Transport.LOAD_COLOR,
            "unload": Transport.UNLOAD_COLOR,
            "both": Transport.BOTH_COLOR
        }
    }

    return render(
        request,
        "transports/week.html",
        context,
    )


@user_passes_test(
    lambda user: user.is_superuser
    or user.has_perm('accounts.daily_view')
    or user.groups.first().custom_group.allowed_views.filter(view="day").exists(),
    None,
    "",
)
def day(request):
    transports = Transport.find_objects_between_timestamps(datetime.today().replace(hour=0, minute=0, second=0), datetime.today().replace(hour=23, minute=59, second=59))
    return render(request, "transports/day.html", {"title_appendix": "Denný pohľad", "transports": transports})


class TableView(UserPassesTestMixin, ListView):
    filterset_class = TransportFilter
    paginate_by = 20
    filterset = None
    template_name = "transports/table.html"

    def test_func(self):
        user = self.request.user
        return (
            user.is_superuser
            or user.groups.first()
            .custom_group.allowed_views.filter(view="table")
            .exists()
        )

    def handle_no_permission(self):
        messages.add_message(
            self.request, messages.ERROR, "Na zobrazenie tejto časti nemáte právomoc."
        )
        return redirect("view_based_on_user_group")

    def get_queryset(self):
        queryset = (
            Transport.objects.all()
            .select_related(
                "supplier", "carrier", "transport_status", "transport_priority", "gate"
            )
            .order_by("-process_start")
        )
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        context["params"] = json.dumps(self.request.GET)
        return context

    def get(self, request, *args, **kwargs):
        if self.request.htmx:
            self.template_name = "transports/elements/table/base.html"

        return super().get(request, *args, **kwargs)


def export(request, _format):
    if _format not in ["csv", "xlsx"]:
        return Http404()

    qs = TransportFilter(
        request.GET,
        Transport.objects.all().select_related(
            "supplier", "carrier", "transport_status", "transport_priority", "gate"
        ),
    ).qs.distinct()
    qs = [_model_to_dict(transport) for transport in qs]

    filepath = _transport_csv_export(qs)
    if _format == "csv":
        return FileResponse(open(filepath, "rb"))

    wb = Workbook()
    with open(filepath, "r") as f:
        for row in csv.reader(f):
            wb.active.append(row)

    wb.save(filepath.with_suffix(".xlsx"))
    return FileResponse(open(filepath.with_suffix(".xlsx"), "rb"))


def _transport_csv_export(qs):
    filepath = pathlib.Path().resolve() / (
        "tmp/export-" + datetime.today().strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    )
    ordered_fieldnames = OrderedDict(
        [(f.name, f.verbose_name) for f in Transport._meta.fields]
    )

    with open(filepath, "x", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=ordered_fieldnames, extrasaction="ignore")

        writer.writerow(ordered_fieldnames)
        writer.writerows(qs)

    return filepath


def _model_to_dict(instance: Transport):
    d = {}
    for f in [x.name for x in Transport._meta.fields]:
        d[f] = getattr(instance, f).__str__()

    return d


def _get_default_transport_data():
    transport_priority = cache.get("default_transport_priority_id")
    if transport_priority is None:
        transport_priority = TransportPriority.objects.filter(is_default=True).first()

        if transport_priority is None:
            raise RuntimeError("No default transport priority!")

        transport_priority = transport_priority.pk

        cache.set("default_transport_priority_id", transport_priority, 600)

    transport_status = cache.get("default_transport_status_id")
    if transport_status is None:
        transport_status = TransportStatus.objects.filter(is_default=True).first()

        if transport_status is None:
            raise RuntimeError("No default transport status!")

        transport_status = transport_status.pk
        cache.set("default_transport_status_id", transport_status, 600)

    return {
        "transport_priority": transport_priority,
        "transport_status": transport_status,
    }
