from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.validators import datetime_not_future
from edc_constants.choices import YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from ..choices import HIV_RESULT, WHY_NO_HIV_TESTING_CHOICE

from .model_mixins import CrfModelMixin


class HivResult(CrfModelMixin):

    hiv_result = models.CharField(
        verbose_name="Today\'s HIV test result",
        max_length=50,
        choices=HIV_RESULT,
        help_text="If participant declined HIV testing, please select a reason below.",
    )

    hiv_result_datetime = models.DateTimeField(
        verbose_name="Today\'s HIV test result date and time",
        null=True,
        blank=True,
        validators=[datetime_not_future],
    )

    blood_draw_type = models.CharField(
        verbose_name="What type of blood was used for the test",
        max_length=15,
        choices=(('capillary', 'Capillary'), ('venous', 'Venous'),
                 (NOT_APPLICABLE, 'Not applicable')),
        default=NOT_APPLICABLE,
        help_text="",
    )

    insufficient_vol = models.CharField(
        verbose_name='If capillary, is the volume less than 350uL?',
        max_length=15,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        help_text=("Note: if capillary blood and less than 350uL,"
                   " an additional venous blood draw is required"),
    )

    why_not_tested = models.CharField(
        verbose_name="What was the main reason why you did not want HIV testing"
                     " as part of today's visit?",
        max_length=65,
        null=True,
        blank=True,
        choices=WHY_NO_HIV_TESTING_CHOICE,
        help_text="Note: Only asked of individuals declining HIV testing during this visit.",
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name = "Today\'s HIV Result"
        verbose_name_plural = "Today\'s HIV Result"
