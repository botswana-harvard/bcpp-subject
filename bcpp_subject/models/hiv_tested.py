from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.fields import OtherCharField

from ..choices import WHERE_HIV_TEST_CHOICE, WHY_HIV_TEST_CHOICE

from .model_mixins import CrfModelMixin
from edc_constants.choices import YES_NO_UNSURE


class HivTested (CrfModelMixin):

    """CS002- for those who have tested for HIV. Its branch off from Q18 - HIV testing History"""

    num_hiv_tests = models.IntegerField(
        verbose_name="How many times before today have you had an HIV test?",
        null=True,
        help_text="",
    )

    where_hiv_test = models.CharField(
        verbose_name="Where were you tested for HIV, the last"
                     " [most recent] time you were tested?",
        max_length=85,
        choices=WHERE_HIV_TEST_CHOICE,
        help_text="",
    )

    where_hiv_test_other = OtherCharField()

    why_hiv_test = models.CharField(
        verbose_name="Not including today's HIV test, which of the following"
                     " statements best describes the reason you were tested the last"
                     " [most recent] time you were tested before today?",
        max_length=105,
        null=True,
        choices=WHY_HIV_TEST_CHOICE,
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
        verbose_name = "HIV Tested"
        verbose_name_plural = "HIV Tested"
