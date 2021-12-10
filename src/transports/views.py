from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .forms import TransportForm
from .utils import TransportChangeTracker
from .models import Transport
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

    if request.method == "POST":
        tracker = TransportChangeTracker(request.POST, get_object_or_404(Transport, pk=pk), request.user)

        if tracker.is_valid():
            tracker.track()
            messages.add_message(
                request, messages.SUCCESS, "Preprava bola úspešne upravená."
            )
        else:
            messages.add_message(
                request, messages.ERROR, "Prepravu sa nepodarilo upraviť. Skontrolujte prosím vyplnené údaje."
            )
            saved = False

        form = tracker.get_form()

    # get instance if primary key is provided
    if form is None:
        try:
            inst = Transport.objects.get(pk=pk)
        except TypeError:
            inst = None

        form = TransportForm(instance=inst)

    context = {"form": form, 'saved': saved}

    if request.user.is_superuser: # if user is administrator, include transport modifications in context
        context['changes'] = TransportModification.objects.filter(transport_id=pk).order_by('created').all()

    return render(request, "transports/elements/form.html", context)


@user_passes_test(lambda user: user.is_superuser or user.groups.first().custom_group.allowed_views.filter(view='week').exists(), None, '')
def week(request):
    return render(request, "transports/week.html")

@user_passes_test(lambda user: user.is_superuser or user.groups.first().custom_group.allowed_views.filter(view='day').exists(), None, '')
def day(request):
    return render(request, "transports/day.html")

@login_required
def detail(request):
    return render(request, "transports/detail.html")

@user_passes_test(lambda user: user.is_superuser or user.groups.first().custom_group.allowed_views.filter(view='table').exists(), None, '')
def table(request):
    return render(request, "transports/table.html")

class TransportListView(ListView):
    template_name = "transports/index.html"
    queryset = Transport.objects.all()
