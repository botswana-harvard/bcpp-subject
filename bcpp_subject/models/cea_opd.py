from django.db import models
from edc_constants.choices import YES_NO, YES_NO_REFUSED

# from ..choices import ENROLMENT_REASON, OPPORTUNISTIC_ILLNESSES
from .model_mixins import CrfModelMixin, CrfModelManager


class CeaOpd (CrfModelMixin):

    care_sought = models.CharField(
        verbose_name="In the last 3 months, did you seek care at a Government"
        "Primary Health Clinic/Post? Not including any"
        " visits for which you were hospitalized",
        max_length=3,
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
        help_text="If yes, indicate which of the following were ordered (choose all relevant answers):")

    lab_tests_performed = models.CharField(
        verbose_name=" For the most recent time that you sought care, were any procedures performed?  ",
        max_length=3,
        choices=YES_NO,
        help_text="")

    lab_test = models.CharField(
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
        choices=YES_NO,
        help_text="")

    further_evaluation = models.CharField(
        verbose_name="For the most recent time that you sought care,"
        " were you referred for further evaluation or treatment?  ",
        max_length=3,
        choices=YES_NO,
        help_text="")

    evaluation_referred = models.CharField(
        verbose_name="If yes, describe what you were referred for, and to whom you were referred.",
        max_length=25,
        help_text="")

    objects = CrfModelManager()

    class Meta(CrfModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name = "CEA  OPD Questions"
