from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_lab.model_mixins import ResultItemModelMixin

from .result import Result


class ResultItem(ResultItemModelMixin, BaseUuidModel):

    result = models.ForeignKey(Result)

    history = HistoricalRecords()

    class Meta:
        app_label = 'edc_lab'
