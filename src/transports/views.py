from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .forms import TransportForm
from .utils import TransportChangeTracker
from transports.models import Transport



ADMIN = "Administrator"
TML = "Transport manazment a Logistika"
PREDAK = "Predak"
SKLADNIK = "Skladnik"

DEFAULT_VIEWS = {
    ADMIN : "tabulka/",    
    TML : "tyzden/",     
    PREDAK : "tyzden/",     
    SKLADNIK : "den/"        
}

@user_passes_test(lambda user: user.groups.filter(name__in=[ADMIN, TML, PREDAK, SKLADNIK]).exists())
def view_based_on_user_group(request):
    return redirect(DEFAULT_VIEWS[request.user.groups.all().first().name])      

@user_passes_test(lambda user: user.groups.filter(name__in=[ADMIN, TML, PREDAK, SKLADNIK]).exists())
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


@user_passes_test(lambda user: user.groups.filter(name__in=[ADMIN, TML, PREDAK]).exists())
def week(request):
    return render(request, "transports/week.html")

@user_passes_test(lambda user: user.groups.filter(name__in=[ADMIN, PREDAK, SKLADNIK]).exists())
def day(request):
    return render(request, "transports/day.html")

@user_passes_test(lambda user: user.groups.filter(name__in=[ADMIN, PREDAK, SKLADNIK]).exists())
def detail(request):
    return render(request, "transports/detail.html")

@user_passes_test(lambda user: user.groups.filter(name=ADMIN).exists())
def table(request):
    return render(request, "transports/table.html")

class TransportListView(ListView):
    template_name = "transports/index.html"
    queryset = Transport.objects.all()
