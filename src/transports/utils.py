import json
import logging
from django.db import transaction
from django.forms.models import model_to_dict

from .forms import TransportForm
from modifications.models import TransportModification
from transports.models import Transport

logger = logging.getLogger(__file__)


class TransportChangeTracker:
    """
    Handles all change tracking on transport model instances.
    """

    save_instance = True

    def __init__(self, data, instance, user, partial=False):
        if partial:
            # enable partial instance update by injecting original instance data
            # to validated data dictionary
            instance_dict = model_to_dict(instance)
            for field in instance_dict:
                if field not in data or data[field] is None:
                    data[field] = instance_dict[field]

        self.instance = instance
        self.form = TransportForm(user, data, instance=instance)
        self.form.apply_restrictions()
        self.user = user

    def get_form(self):
        return self.form

    def is_valid(self):
        return self.form.is_valid()

    def set_save_instance(self, value):
        self.save_instance = value

    @transaction.atomic
    def track(self):
        """
        Track changes on Transport model instances.
        """
        self.obj = self.form.save(commit=False)

        if len(self.obj.tracker.changed()) > 0:

            # track changes from form values
            changes = {}
            for field, value in self.obj.tracker.changed().items():
                if value != getattr(self.obj, field):
                    before, after = self._get_value(
                        self.obj, field, value
                    ), self._get_value(self.obj, field)
                    changes[field] = {"BEFORE": before, "AFTER": after}

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

    def _get_value(self, instance, field, override_value=None):
        """
        Get instance's field value. Related fields (FK, M2M) return name of the related
        model instance.
        """
        if "id" not in field:
            return (
                override_value
                if override_value is not None
                else getattr(instance, field)
            )

        related_model = getattr(Transport, field).descriptor.field.related_model
        instances = related_model.fetch_instances()

        # if we don't want to access actual value in instance, but use the
        # provided one
        instance_id = (
            override_value if override_value is not None else getattr(instance, field)
        )

        return instances.get(instance_id, instance_id)
