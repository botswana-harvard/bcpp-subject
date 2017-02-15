from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_base.model.fields import OtherCharField

from ..choices import (
    KEPT_APPT, TYPE_OF_EVIDENCE,
    RECOMMENDED_THERAPY, REASON_RECOMMENDED, REASONS_INITIATED)

from .model_mixins import CrfModelMixin


class HivLinkageToCare (CrfModelMixin):

    kept_appt = models.CharField(
        verbose_name=(
            'When we last saw you in {previous} we scheduled an appointment '
            'for you in an HIV care clinic on {referral_appt_date}. '
            'Did you keep that appointment?'),
        max_length=50,
        choices=KEPT_APPT,
        null=True,
        help_text='')

    different_clinic = models.CharField(
        verbose_name='If went to a different clinic, specify the clinic',
        default=None,
        null=True,
        blank=True,
        max_length=50,
        help_text=''
    )

    failed_attempt_date = models.DateField(
        verbose_name=(
            'If you tried to attend an HIV care clinic and '
            'left before you saw a healthcare provider, specify the date?'),
        default=None,
        null=True,
        blank=True,
        help_text=''
    )

    first_attempt_date = models.DateField(
        verbose_name=('What was the date when you first went '
                      'to the community_name clinic?'),
        default=None,
        null=True,
        blank=True,
        help_text=''
    )

    evidence_referral = models.CharField(
        verbose_name='Type of Evidence:',
        max_length=50,
        choices=TYPE_OF_EVIDENCE,
        null=True,
        help_text='')

    evidence_referral_other = OtherCharField()

    recommended_art = models.CharField(
        verbose_name=(
            '[IF PERSON WAS ART NAIVE OR A DEFAULTER AT LAST INTERVIEW] '
            'Since the last time we spoke with '
            'you on last_visit_date, has a doctor/nurse or '
            'other healthcare worker recommended '
            'that you start antiretroviral therapy (ARVs), a '
            'combination of medicines to treat your HIV infection?'),
        max_length=50,
        choices=RECOMMENDED_THERAPY,
        null=True,
        help_text='If No [SKIP TO #10]')

    reason_recommended_art = models.CharField(
        verbose_name='If yes, do you know why ARVs were recommended?',
        max_length=50,
        choices=REASON_RECOMMENDED,
        null=True,
        blank=True,
        help_text='')

    reason_recommended_art_other = OtherCharField()

    initiated = models.CharField(
        verbose_name=(
            '[IF PERSON WAS ART NAIVE OR A DEFAULTER AT LAST INTERVIEW] '
            'Did you [start/restart] ART since we '
            'spoke with you on last_visit_date?'),
        max_length=50,
        choices=REASONS_INITIATED,
        null=True,
        help_text='If NO [SKIP TO #9]')

    initiated_date = models.DateField(
        verbose_name='When did you [start/restart] ART?',
        default=None,
        null=True,
        blank=True,
        help_text=''
    )

    initiated_clinic = models.CharField(
        verbose_name='Which clinic facility did you start/restart ART at?',
        max_length=25,
        help_text='Indicate the name of the clinic')

    initiated_clinic_other = OtherCharField()

    initiated_clinic_community = models.CharField(
        verbose_name=('[If Clinic is not the referred clinic] '
                      'In which community is this clinic located'),
        null=True,
        max_length=50,
        help_text='Indicate the community name'
    )

    evidence_art = models.CharField(
        verbose_name='Type of Evidence:',
        max_length=50,
        choices=TYPE_OF_EVIDENCE,
        null=True,
        help_text='')

    evidence_art_other = OtherCharField()

    history = HistoricalRecords()

    def last_community(self, request):
        return self.subject_visit.household_member.household_structure.household.plot

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = 'Hiv Linkage To Care'
        verbose_name_plural = 'Hiv Linkage To Care'
