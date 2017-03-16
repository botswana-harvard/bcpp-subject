from django.db import models

from edc_base.model_managers import HistoricalRecords
from edc_base.model_validators import datetime_not_future
from edc_constants.constants import NOT_APPLICABLE

from ..choices import EASY_OF_USE, QUANTIFIER
from .model_mixins import CrfModelMixin, MobileTestModelMixin

MOBILE = 'mobile setting'

TEST_LOCATION = (
    (MOBILE, 'Mobile Setting'),
    ('household setting', 'Household Setting'),
    (NOT_APPLICABLE, 'Not applicable'),
)


class PimaVl(MobileTestModelMixin, CrfModelMixin):

    location = models.CharField(
        verbose_name='Where was this test done',
        choices=TEST_LOCATION,
        max_length=25,
        default=MOBILE,
    )

    quantifier = models.CharField(
        choices=QUANTIFIER,
        max_length=25,
        null=True,
        blank=True,
    )

    test_datetime = models.DateTimeField(
        verbose_name='Test started at',
        validators=[datetime_not_future],
        null=True,
        blank=True,
    )

    easy_of_use = models.CharField(
        verbose_name='Ease of use by field operator?',
        max_length=25,
        choices=EASY_OF_USE,
        null=True,
        blank=True,
    )

    stability = models.TextField(
        verbose_name='Stability',
        max_length=250,
        null=True,
        blank=True,
        help_text='Comment')

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = 'POC VL'
        verbose_name_plural = 'POC VL'
