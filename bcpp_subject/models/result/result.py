from django.db import models
from django.db.models.deletion import PROTECT

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_lab.model_mixins.result import ResultModelMixin

from ..subject_requisition import SubjectRequisition


class Result(ResultModelMixin, BaseUuidModel):

    requisition = models.ForeignKey(SubjectRequisition, on_delete=PROTECT)

    history = HistoricalRecords()

    class Meta:
        app_label = 'edc_lab'
