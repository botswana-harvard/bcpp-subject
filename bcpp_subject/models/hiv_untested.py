from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO_UNSURE

from ..choices import WHY_NO_HIV_TESTING_CHOICE

from .model_mixins import CrfModelMixin


class HivUntested (CrfModelMixin):

    """CS002- for those who have NOT tested for HIV. Its
    branch off from Q18 - HIV testing History"""

    why_no_hiv_test = models.CharField(
        verbose_name="If you were not tested for HIV in the 12 months prior"
                     " to today, what is the main reason why not?",
        max_length=55,
        null=True,
        choices=WHY_NO_HIV_TESTING_CHOICE,
        help_text="",
    )

    hiv_pills = models.CharField(
        verbose_name="Have you ever heard about treatment for"
                     " HIV with pills called antiretroviral therapy or ARVs [or HAART]?",
        max_length=25,
        choices=YES_NO_UNSURE,
        null=True,
    )

    arvs_hiv_test = models.CharField(
        verbose_name="Do you believe that treatment for HIV with "
                     "antiretroviral therapy (or ARVs) can help HIV-positive people"
                     " to live longer?",
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_UNSURE,
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "HIV Untested"
        verbose_name_plural = "HIV Untested"
