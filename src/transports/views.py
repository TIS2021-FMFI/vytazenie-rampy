from django.shortcuts import render

from .forms import TransportForm

# Create your views here.
def form(request):
    if request.method == "POST":
        ...
        # TODO: vytvorenie/update transportu z formu a trackovanie zmien

    _form = TransportForm()
    return render(request, "transports/form.html", {"form": _form})
