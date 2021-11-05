import json

from django.shortcuts import render
from modifications.models import TransportModification
from transports.models import Transport
from .forms import TransportForm

from django.views.generic import ListView

# Create your views here.
def form(request):
    _form = TransportForm(request.POST or None)
    if request.method == "POST" and _form.is_valid():
        obj = _form.save(commit=False)
        print(request.user)
        if len(obj.tracker.changed()) > 0:
            changes = {}
            for k, v in obj.tracker.changed().items():
                changes[k] = {"BEFORE": v, "AFTER": getattr(obj, k)}
            obj.save()
            TransportModification.objects.create(
                transport=obj,
                user=request.user,
                changes=json.dumps(
                    changes, default=str
                ),  # default=str kedze datetime neni serializable
            ).save()

    return render(request, "transports/form.html", {"form": _form})


class TransportListView(ListView):
    template_name = "transports/index.html"
    queryset = Transport.objects.all()
