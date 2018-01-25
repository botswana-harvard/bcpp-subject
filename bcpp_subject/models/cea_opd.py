from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_base.model_fields.custom_fields import OtherCharField
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO, YES_NO_NA

from .list_models import TestsOrdered, MedicationPrescribed
from .model_mixins import CrfModelMixin, CrfModelManager


class CeaOpd (CrfModelMixin):

    times_care_sought = models.IntegerField(
        verbose_name=(
            "In the last 3 months, how many times did you seek care"
            " at a Government Primary Health Clinic/Post?"))

    times_care_obtained = models.IntegerField(
        verbose_name=(
            "Of the times you sought care, how many times were you able to "
            "obtain care?"))

    tb_care = models.IntegerField(
        verbose_name=(
            "Of the times you sought care, how many times were you seeking "
            "care for TB Diagnosis or Treatment?"))

    hiv_related = models.IntegerField(
        verbose_name=(
            "Of the times you sought care, how many times were you seeking "
            "care for Routine HIV-related care?"),
        help_text="(such as ART start, refill,routine"
        "monitoring")

    hiv_related_none_tb = models.IntegerField(
        verbose_name=(
            "Of the times you sought care, how many times were you seeking "
            "Diagnosis or Treatment of HIV-related illness other than?"))

    pregnancy_related = models.IntegerField(
        verbose_name=(
            "Of the times you sought care, how many times were you seeking "
            "care for Pregnancy related care?"),
        help_text="Pregnancy related care (e.g. antenatal, postnatal care")

    injury_accident = models.IntegerField(
        verbose_name=(
            "Of the times you sought care, how many times were you seeking"
            "care for Injury or Accident?"))

    chronic_disease = models.IntegerField(
        verbose_name=(
            "Of the times you sought care, how many times were you seeking"
            "care for Chronic disease-related care?"),
        help_text="Chronic disease-related care(e.g high blood pressure,"
        "diabetes, depression")

    cancer_care = models.IntegerField(
        verbose_name=(
            "Of the times you sought care, how many times were you seeking"
            "care for Cancer diagnosis, treatment?"))

    other_care = OtherCharField(
        null=True,
        blank=True,
        verbose_name='If other medical care, please specify:',
        max_length=15)

    other_care_count = OtherCharField(
        null=True,
        blank=True,
        verbose_name=("If other, please specify the number of times care sort"
                      "for other medical care:"),
        max_length=15)

    marriage_certificate_no = models.CharField(
        verbose_name=("What is the marriage certificate number?"),
        max_length=9,
        null=True,
        blank=True,
        help_text="e.g. 000/YYYY")

    lab_tests_ordered = models.CharField(
        verbose_name=(
            "For the most recent time that you sought care, were any lab"
            "tests ordered?"),
        max_length=3,
        choices=YES_NO)

    tests_ordered = models.ManyToManyField(
        TestsOrdered,
        related_name='tests_ordered',
        blank=True,
        verbose_name="If yes, indicate which of the following were ordered.")

    ordered_other = OtherCharField(
        null=True,
        blank=True,
        verbose_name='If other, please specify:',
        max_length=15)

    procedures_performed = models.CharField(
        verbose_name=" For the most recent time that you sought care, were"
        "any procedures performed? ",
        max_length=3,
        choices=YES_NO_NA)

    procedure = models.CharField(
        verbose_name="If yes, describe:",
        max_length=25,
        null=True,
        blank=True)

    medication = models.CharField(
        verbose_name="For the most recent time that you sought care, were"
        "any medications prescribed?",
        max_length=6,
        choices=YES_NO_NA)

    medication_prescribed = models.ManyToManyField(
        MedicationPrescribed,
        related_name='medication_prescribed',
        blank=True,
        verbose_name="If yes,indicate which of the following were prescribed.")

    prescribed_other = OtherCharField(
        null=True,
        blank=True,
        verbose_name='If other, please specify:',
        max_length=15)

    further_evaluation = models.CharField(
        verbose_name="For the most recent time that you sought care,"
        " were you referred for further evaluation or treatment?",
        max_length=3,
        choices=YES_NO_NA)

    evaluation_referred = models.CharField(
        verbose_name="If yes, describe what you were referred for, and to"
        "whom you were referred.",
        max_length=50,
        blank=True)

    cd4_date = models.DateField(
        verbose_name='Date of most recent CD4 count',
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text='For HIV-infected participants')

    cd4_result = models.IntegerField(
        verbose_name='Result of most recent CD4 count',
        validators=[MinValueValidator(1), MaxValueValidator(999)],
        null=True,
        blank=True,
        help_text='For HIV-infected participants, in units/mm^3')

    objects = CrfModelManager()

    class Meta(CrfModelMixin.Meta):
        app_label = "bcpp_subject"
        verbose_name = "CEA  OPD Question"
