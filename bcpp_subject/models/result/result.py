from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_lab.model_mixins import ResultModelMixin

from ..subject_requisition import SubjectRequisition


class Result(ResultModelMixin, BaseUuidModel):

    requisition = models.ForeignKey(SubjectRequisition)

    history = HistoricalRecords()

    class Meta:
        app_label = 'edc_lab'
