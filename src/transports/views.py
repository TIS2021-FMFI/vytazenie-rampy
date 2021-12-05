import json

from django.shortcuts import render, get_object_or_404
from modifications.models import TransportModification
from transports.models import Transport
from .forms import TransportForm


from django.views.generic import ListView

def form(request, pk=None):
    """
    Create new Transport and update existing one. Track changes made on Transports
    along with user who submitted them.
    """
    if request.method == "POST":

        _form = TransportForm(
            request.POST, instance=get_object_or_404(Transport, pk=pk)
        )

        if _form.is_valid():
            obj = _form.save(commit=False)

            if len(obj.tracker.changed()) > 0:

                # track changes from form values
                changes = {}
                for field, value in obj.tracker.changed().items():
                    changes[field] = {"BEFORE": value, "AFTER": getattr(obj, field)}

                obj.save()

                # create change log
                TransportModification.objects.create(
                    transport=obj,
                    user=request.user,
                    changes=json.dumps(
                        changes, default=str
                    ),  # default=str kedze datetime neni serializable
                ).save()
    else:
        # get instance if primary key is provided
        try:
            inst = Transport.objects.get(pk)
        except TypeError:
            inst = None

        _form = TransportForm(instance=inst)

    return render(request, "transports/form.html", {"form": _form})

def week(request):
    return render(request, "transports/week.html")


class TransportListView(ListView):
    template_name = "transports/index.html"
    queryset = Transport.objects.all()
