from django.db import models

from django.core.validators import MinValueValidator, RegexValidator

from edc_base.model_fields import OtherCharField
from edc_base.model_validators import datetime_not_future
from edc_constants.choices import YES_NO

from ...choices import PIMA


class MobileTestModelMixin(models.Model):

    test_done = models.CharField(
        verbose_name="Was the test done today?",
        choices=YES_NO,
        max_length=3)

    reason_not_done = models.CharField(
        verbose_name="If test not done, please explain why",
        max_length=50,
        choices=PIMA,
        null=True,
        blank=True)

    reason_not_done_other = OtherCharField(
        max_length=50)

    machine_identifier = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex='\d+', message='Machine ID must be a two digit number.')],
        null=True,
        blank=True,
        help_text="type this id directly from the machine as labeled")

    result_datetime = models.DateTimeField(
        verbose_name="Result Date and time",
        validators=[datetime_not_future],
        null=True,
        blank=True)

    result_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True)

    comment = models.TextField(
        max_length=250,
        null=True,
        blank=True)

    class Meta:
        abstract = True
