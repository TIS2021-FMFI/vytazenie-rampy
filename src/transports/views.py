import json
import pathlib
import csv
import logging
import time
import copy

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
        inst = Transport.objects.select_related(
            "supplier", "carrier", "transport_priority", "transport_status", "gate"
        ).get(pk=pk)
    except Transport.DoesNotExist:
        # create new instance with initial data
        inst = Transport(**_get_default_transport_data())

    if request.method == "POST":
        tracker = TransportChangeTracker(
            copy.deepcopy(request.POST), inst, request.user
        )

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
        _form = TransportForm(request.user, instance=inst)

    context = {"form": _form, "saved": saved}

    if request.user.is_superuser and request.method == "GET":
        # if user is administrator, include transport modifications in context
        changes = tuple(
            TransportModification.objects.filter(transport_id=pk)
            .order_by("created")
            .all()
        )

        # first fetch from cache, if not available, parse changes
        cache_key = "transport_modifications_" + str(hash(changes))
        changes_cached = cache.get(cache_key)
        if changes_cached is not None:
            context.update(changes_cached)
        else:
            context["changes_parsed"] = []

            # iterate through individual transport modifications (changes)
            for index, change in enumerate(changes):
                changes_dict = json.loads(change.changes)
                context["changes_parsed"].append(
                    {
                        "date": change.created,
                        "user": str(change.user),
                        "changes": _parse_transport_modification_changes(
                            changes_dict, index == 0
                        ),
                    }
                )

            # latest changes display next to the form label
            context["latest_changes"] = _create_latest_changes(changes)
            cache.set(
                cache_key,
                {
                    "latest_changes": context["latest_changes"],
                    "changes_parsed": context["changes_parsed"],
                },
            )

    return render(request, "transports/elements/form.html", context)


def _parse_transport_modification_changes(changes, creation_change=False):
    """
    Parses changes on all fields into sentences, that get displayed on the frontend.
    """
    changes_str = []

    for field in changes:
        field_name = Transport._meta.get_field(field).verbose_name

        before, after = _format_change_value(
            changes[field]["BEFORE"]
        ), _format_change_value(changes[field]["AFTER"])

        # if this is the creation change (modification created on transport creation)
        # do not display original value
        changes_str.append(
            f"{field_name}: {before} -> {after}"
            if not creation_change
            else f"{field_name}: {after}"
        )

    return changes_str


def _format_change_value(value):
    """
    Format values in displayed changes.
    """
    try:
        return Transport._format_datetime(parser.parse(value))
    except:
        if isinstance(value, bool):
            return "áno" if value else "nie"
        if value is None:
            return "-"

        return value


def _create_latest_changes(changes):
    """
    Get last change on individual Transport fields.
    """
    last_changes = { f.name: None for f in Transport._meta.fields if f.name != 'id' }

    for change in reversed(changes[1:]):
        changes_dict = json.loads(change.changes)

        for field in changes_dict:
            field_name = field

            if isinstance(field, str):
                field_name = field.replace("_id", "")

            if last_changes[field_name] is not None:
                continue

            before = changes_dict[field]["BEFORE"]
            after = changes_dict[field]["AFTER"]

            last_changes[
                field_name
            ] = f"{str(change.user)}: {_format_change_value(before)} -> {_format_change_value(after)}"

            # if last changes are found for all fields, don't continue
            if all([x is not None for x in last_changes.values()]):
                return last_changes

    return last_changes


@user_passes_test(
    lambda user: user.is_authenticated
        and (user.is_superuser
        or user.has_perm("accounts.weekly_view")
        or user.groups.first().custom_group.allowed_views.filter(view="week").exists()),
    None,
    "",
)
def week(request):
    context = {
        "title_appendix": "Týždenný pohľad",
        "calendar_controls": True,
        "color_helper": {
            "load": Transport.LOAD_COLOR,
            "unload": Transport.UNLOAD_COLOR,
            "both": Transport.BOTH_COLOR,
        },
    }

    return render(
        request,
        "transports/week.html",
        context,
    )


@user_passes_test(
    lambda user: user.is_authenticated
        and (user.is_superuser
        or user.has_perm("accounts.daily_view")
        or user.groups.first().custom_group.allowed_views.filter(view="day").exists()),
    None,
    "",
)
def day(request):
    # find transports only from the current day
    transports = (
        Transport.find_objects_between_timestamps(
            datetime.today().replace(hour=0, minute=0, second=0),
            datetime.today().replace(hour=23, minute=59, second=59),
        )
        .select_related(
            "gate", "supplier", "carrier", "transport_priority", "transport_status"
        )
        .order_by("process_start")
        .filter(canceled=False)
    )

    # active transport is the one that gets activated on frontend
    active_transport_id = None
    if request.GET.get("active_transport_id"):
        active_transport_id = int(request.GET.get("active_transport_id"))

    return render(
        request,
        "transports/elements/day/content.html"
        if request.htmx
        else "transports/day.html",
        {
            "title_appendix": "Denný pohľad",
            "transports": transports,
            "active_transport_id": active_transport_id,
        },
    )


class TableView(UserPassesTestMixin, ListView):
    filterset_class = TransportFilter
    paginate_by = 20
    filterset = None
    template_name = "transports/table.html"

    def test_func(self):
        """
        Check whether the table view can be displayed to current user.
        """
        user = self.request.user
        return (
            user.is_authenticated
            and (user.is_superuser
            or user.groups.first()
            .custom_group.allowed_views.filter(view="table")
            .exists())
        )

    def handle_no_permission(self):
        """
        Gets called when user does not pass the test function.
        """
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
        # if request was made from HTMX, use only partial template
        if self.request.htmx:
            self.template_name = "transports/elements/table/base.html"

        return super().get(request, *args, **kwargs)


def export(request, _format):
    if _format not in ["csv", "xlsx"]:
        return Http404()

    # fetch all transports that correspond to filters
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

    # create excel export from already existing csv one
    wb = Workbook()
    with open(filepath, "r") as f:
        for row in csv.reader(f):
            wb.active.append(row)

    wb.save(filepath.with_suffix(".xlsx"))
    return FileResponse(open(filepath.with_suffix(".xlsx"), "rb"))


def _transport_csv_export(qs):
    """
    Create CSV export from provided queryset.
    """
    filepath = pathlib.Path().resolve() / (
        "tmp/export-" + datetime.today().strftime("%Y-%m-%d-%H-%M-%S") + ".csv"
    )

    # define fields
    ordered_fieldnames = OrderedDict(
        [(f.name, f.verbose_name) for f in Transport._meta.fields]
    )

    # encoding set to utf-8-sig so that excel will now the encoding right away
    with open(filepath, "x", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=ordered_fieldnames, extrasaction="ignore")

        #header
        writer.writerow(ordered_fieldnames)

        #transports
        writer.writerows(qs)

    return filepath


def _model_to_dict(instance: Transport):
    """
    Custom model to dict function, since the django one creates
    *_id fields from relation fields, however we need names.
    """
    d = {}
    for f in [x.name for x in Transport._meta.fields]:
        d[f] = getattr(instance, f).__str__()

    return d


def _get_default_transport_data():
    """
    Prefill form (Transport instance) with initial default values.
    """
    transport_priority_id = cache.get("default_transport_priority_id")
    if transport_priority_id is None:
        transport_priority = TransportPriority.objects.filter(is_default=True).first()

        if transport_priority is None:
            raise RuntimeError("No default transport priority!")

        transport_priority_id = transport_priority.pk

        cache.set("default_transport_priority_id", transport_priority_id, 600)

    transport_status_id = cache.get("default_transport_status_id")
    if transport_status_id is None:
        transport_status = TransportStatus.objects.filter(is_default=True).first()

        if transport_status is None:
            raise RuntimeError("No default transport status!")

        transport_status_id = transport_status.pk
        cache.set("default_transport_status_id", transport_status_id, 600)

    return {
        "transport_priority_id": transport_priority_id,
        "transport_status_id": transport_status_id,
    }
