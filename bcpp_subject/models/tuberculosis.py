from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_future

from ..choices import DX_TB_CHOICE

from .model_mixins import CrfModelMixin


class Tuberculosis (CrfModelMixin):

    """A model completed by the user to record any diagnosis of
    Tuberculosis in the past 12 months."""

    tb_date = models.DateField(
        verbose_name="Date of the diagnosis of tuberculosis:",
        validators=[date_not_future],
        help_text="",
    )

    tb_dx = models.CharField(
        verbose_name="[Interviewer:]What is the tuberculosis diagnosis as recorded?",
        max_length=50,
        choices=DX_TB_CHOICE,
        help_text="",
    )
    tb_dx_other = OtherCharField(
        null=True,
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Tuberculosis"
        verbose_name_plural = "Tuberculosis"
