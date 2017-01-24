from django.db import models

from edc_base.model.models import HistoricalRecords

from .model_mixins import CrfModelMixin, CrfModelManager

ARVS = (('something', 'something'), )


class ArvHistory (CrfModelMixin):

    """A model completed by the user to capture prior ARV history.

    See also: model `HivCarAdherence`.
    """

    # TODO: populate on the form from the ArvRegimen table
    # FIXME:
    arv = models.CharField(
        max_length=25,
        choices=ARVS)

    date_started = models.DateField(
        null=True)

    date_stopped = models.DateField(
        null=True)

    manager = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
