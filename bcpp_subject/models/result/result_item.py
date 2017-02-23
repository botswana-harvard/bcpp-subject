from django.db import models
from django.db.models.deletion import PROTECT

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_lab.model_mixins import ResultItemModelMixin

from .result import Result


class ResultItem(ResultItemModelMixin, BaseUuidModel):

    result = models.ForeignKey(Result, on_delete=PROTECT)

    history = HistoricalRecords()

    class Meta:
        app_label = 'edc_lab'
