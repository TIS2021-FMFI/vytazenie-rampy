from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from .forms import TransportForm
from .utils import TransportChangeTracker
from transports.models import Transport


from django.views.generic import ListView

def form(request, pk=None):
    """
    Create new Transport and update existing one. Track changes made on Transports
    along with user who submitted them.
    """
    form = None

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

        form = tracker.get_form()
        # get instance if primary key is provided

    if form is None:
        try:
            inst = Transport.objects.get(pk)
        except TypeError:
            inst = None

        form = TransportForm(instance=inst)

    return render(request, "transports/form.html", {"form": form})

def week(request):
    return render(request, "transports/week.html")


class TransportListView(ListView):
    template_name = "transports/index.html"
    queryset = Transport.objects.all()
