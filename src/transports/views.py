from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.shortcuts import render, redirect
from .forms import TransportForm
from .utils import TransportChangeTracker
from .models import Transport, TransportPriority, TransportStatus
from modifications.models import TransportModification


@login_required
def view_based_on_user_group(request):
    return redirect(request.user.groups.first().custom_group.default_view.view)


@login_required
def form(request, pk=None):
    """
    Create new Transport and update existing one. Track changes made on Transports
    along with user who submitted them.
    """
    form = None
    saved = True

    try:
        inst = Transport.objects.get(pk=pk)
    except:
        inst = None

    if request.method == "POST":
        tracker = TransportChangeTracker(request.POST, inst, request.user)

        if tracker.is_valid():
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
            saved = False

        form = tracker.get_form()

    # get instance if primary key is provided
    if form is None:
        form = TransportForm(instance=inst, initial=_get_default_transport_data())

    context = {"form": form, "saved": saved}

    if request.user.is_superuser:
        # if user is administrator, include transport modifications in context
        context["changes"] = (
            TransportModification.objects.filter(transport_id=pk)
            .order_by("created")
            .all()
        )

    return render(request, "transports/elements/form.html", context)


@user_passes_test(
    lambda user: user.is_superuser
    or user.groups.first().custom_group.allowed_views.filter(view="week").exists(),
    None,
    "",
)
def week(request):
    return render(request, "transports/week.html")


@user_passes_test(
    lambda user: user.is_superuser
    or user.groups.first().custom_group.allowed_views.filter(view="day").exists(),
    None,
    "",
)
def day(request):
    return render(request, "transports/day.html")


@login_required
def detail(request):
    return render(request, "transports/detail.html")


@user_passes_test(
    lambda user: user.is_superuser
    or user.groups.first().custom_group.allowed_views.filter(view="table").exists(),
    None,
    "",
)
def table(request):
    return render(request, "transports/table.html")

def _get_default_transport_data():
    transport_priority = cache.get('default_transport_priority')
    if transport_priority is None:
        transport_priority = TransportPriority.objects.filter(is_default=True).first()

        if transport_priority is None:
            raise RuntimeError("No default transport priority!")

        transport_priority = transport_priority.pk

        cache.set('default_transport_priority_id', transport_priority, 600)

    transport_status = cache.get('default_transport_status')
    if transport_status is None:
        transport_status = TransportStatus.objects.filter(is_default=True).first()

        if transport_status is None:
            raise RuntimeError("No default transport status!")

        transport_status = transport_status.pk
        cache.set('default_transport_status_id', transport_status, 600)

    return {
        "transport_priority": transport_priority,
        "transport_status": transport_status
    }


