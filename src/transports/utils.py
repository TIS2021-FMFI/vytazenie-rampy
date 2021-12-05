import json
from django.forms.models import model_to_dict

from .forms import TransportForm
from modifications.models import TransportModification

class TransportChangeTracker:
    save_instance = True

    def __init__(self, data, instance, user, partial=False):
        if partial:
            # enable partial instance update by injecting original instance data
            # to validated data dictionary
            instance_dict = model_to_dict(instance)
            for field in instance_dict:
                if field not in data:
                    data[field] = instance_dict[field]

        self.form = TransportForm(data, instance=instance)
        self.user = user

    def is_valid(self):
        return self.form.is_valid()

    def set_save_instance(self, value):
        self.save_instance = value

    def track(self):
        self.obj = self.form.save(commit=False)

        if len(self.obj.tracker.changed()) > 0:

            # track changes from form values
            changes = {}
            for field, value in self.obj.tracker.changed().items():
                changes[field] = {"BEFORE": value, "AFTER": getattr(self.obj, field)}

            if self.save_instance:
                self.obj.save()

            # create change log
            TransportModification.objects.create(
                transport=self.obj,
                user=self.user,
                changes=json.dumps(
                    changes, default=str
                ),  # default=str kedze datetime neni serializable
            ).save()