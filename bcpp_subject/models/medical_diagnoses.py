from django.db import models

from edc_base.model_managers import HistoricalRecords
from edc_constants.choices import YES_NO_DWTA

from .list_models import Diagnoses
from .model_mixins import CrfModelMixin


class MedicalDiagnoses (CrfModelMixin):

    """A model completed by the user to record any major
    illnesses in the past 12 months.
    """

    diagnoses = models.ManyToManyField(
        Diagnoses,
        verbose_name=(
            'Do you recall or is there a record of having any of the '
            'following serious illnesses?'),
    )

    heart_attack_record = models.CharField(
        verbose_name=(
            'Is a record (OPD card, discharge summary) of '
            'a heart disease or stroke diagnosis available to review?'),
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
    )

    cancer_record = models.CharField(
        verbose_name=('Is a record (OPD card, discharge summary) of a '
                      'cancer diagnosis available to review?'),
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
    )

    tb_record = models.CharField(
        verbose_name=(
            'Is a record (OPD card, discharge summary, TB card) of a '
            'tuberculosis infection available to review?'),
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
    )

    sti_record = models.CharField(
        verbose_name=(
            'Is a record (OPD card, discharge summary, ) of an STI '
            'available to review?'),
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = 'Medical Diagnoses'
        verbose_name_plural = 'Medical Diagnoses'
