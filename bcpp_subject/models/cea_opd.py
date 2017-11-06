from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO, YES_NO_REFUSED

from ..choices import TESTS_ORDERED, MEDICATION_PRESCRIBED
from .model_mixins import CrfModelMixin, CrfModelManager


class CeaOpd (CrfModelMixin):

    care_sought = models.CharField(
        verbose_name="In the last 3 months, did you seek care at a Government"
        "Primary Health Clinic/Post? Not including any"
        " visits for which you were hospitalized",
        max_length=7,
        choices=YES_NO_REFUSED,
        help_text="")

    times_care_sought = models.IntegerField(
        verbose_name=(
            "In the last 3 months, how many times did you seek care"
            " at a Government Primary Health Clinic/Post?"),
        help_text="")

    times_care_obtained = models.IntegerField(
        verbose_name=(
            "Of the times you sought care, how many times were you able to obtain care?"),
        help_text="")

    marriage_certificate_no = models.CharField(
        verbose_name=("What is the marriage certificate number?"),
        max_length=9,
        null=True,
        blank=True,
        help_text="e.g. 000/YYYY")

    lab_tests_ordered = models.CharField(
        verbose_name=(
            "For the most recent time that you sought care, were any lab tests ordered? "),
        max_length=3,
        choices=YES_NO,
        help_text="If yes, indicate which of the following were ordered ")

    tests_ordered = models.CharField(
        max_length=25,
        choices=TESTS_ORDERED,
        help_text="")

    ordered_other = OtherCharField(
        null=True,
        blank=True,
        verbose_name='If other, please specify:',
        max_length=15)

    procedures_performed = models.CharField(
        verbose_name=" For the most recent time that you sought care, were any procedures performed?  ",
        max_length=3,
        choices=YES_NO,
        help_text="")

    procedure = models.CharField(
        verbose_name="If yes, describe ",
        max_length=25,
        help_text="")

    medication = models.CharField(
        verbose_name="For the most recent time that you sought care, were any medications prescribed? ",
        max_length=6,
        choices=YES_NO,
        help_text="")

    medication_prescribed = models.CharField(
        verbose_name=(
            "If yes, indicate which of the following were prescribed "),
        max_length=50,
        choices=MEDICATION_PRESCRIBED,
        help_text="")

    prescribed_other = OtherCharField(
        null=True,
        blank=True,
        verbose_name='If other, please specify:',
        max_length=15)

    further_evaluation = models.CharField(
        verbose_name="For the most recent time that you sought care,"
        " were you referred for further evaluation or treatment?  ",
        max_length=3,
        choices=YES_NO,
        help_text="")

    evaluation_referred = models.CharField(
        verbose_name="If yes, describe what you were referred for, and to whom you were referred.",
        max_length=50,
        help_text="")

    cd4_date = models.DateField(
        verbose_name='date of CD4 count for HIV-infected participants',
        validators=[date_not_future],
        null=True,
        blank=True)

    cd4_result = models.IntegerField(
        verbose_name='CD4 Result',
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        null=True,
        help_text='in units/mm^3')

    objects = CrfModelManager()

    class Meta(CrfModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name = "CEA  OPD Question"
