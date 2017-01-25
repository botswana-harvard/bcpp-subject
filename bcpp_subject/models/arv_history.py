from django.db import models

from edc_base.model.models import HistoricalRecords

from .list_models import Arv
from .model_mixins import CrfModelMixin, CrfModelManager


class ArvHistory (CrfModelMixin):

    """A model completed by the user to capture prior ARV history.

    See also: model `HivCareAdherence`.
    """

    arv = models.ForeignKey(
        Arv, on_delete=models.PROTECT, to_field='short_name')

    date_started = models.DateField(
        null=True)

    date_stopped = models.DateField(
        null=True)

    manager = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
