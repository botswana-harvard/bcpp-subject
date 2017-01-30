from django.db import models
from django.core.validators import RegexValidator

from edc_base.model.models import HistoricalRecords
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_future
from edc_constants.choices import YES_NO_DWTA, YES_NO

from ..choices import (
    WHY_NO_ARV_CHOICE, ADHERENCE_4DAY_CHOICE,
    ADHERENCE_4WK_CHOICE, NO_MEDICAL_CARE, WHY_ARV_STOP_CHOICE,
    YES_NO_REGIMEN, SOURCE_EVIDENCE)
from ..models.list_models import Arv, HospitalizationReason, ChronicDisease
from .model_mixins import CrfModelMixin


class HivCareAdherence (CrfModelMixin):
    """"A model completed by the user on the participant's access to
    and adherence to HIV care.
    """

    # filled by is hiv care adherence data already in the system
    first_positive = models.DateField(
        verbose_name='When was your first positive HIV test result?',
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text=(
            'Note: If participant does not want to answer, leave blank. '
            'If participant is unable to estimate date, leave blank.'),
    )

    # longitudinal, terminal value = YES
    medical_care = models.CharField(
        verbose_name=('Have you ever received HIV-related medical or clinical'
                      ' care, for such things as a CD4 count (masole), '
                      'IDCC/ PMTCT registration, additional clinic-based '
                      'counseling?'),
        max_length=25,
        choices=YES_NO_DWTA,
        null=True,
        blank=True,
        help_text='if \'YES\', answer HIV medical care section',
    )

    # longitudinal, always BLANK
    no_medical_care = models.CharField(
        verbose_name=('What is the main reason you have not received '
                      'HIV-related medical or clinical care?'),
        max_length=70,
        null=True,
        blank=True,
        choices=NO_MEDICAL_CARE,
        help_text='',
    )
    no_medical_care_other = OtherCharField()

    # longitudinal, YES if terminal value of medical_care  = YES
    ever_recommended_arv = models.CharField(
        verbose_name=(
            'Have you ever been recommended by a doctor/nurse or other '
            'healthcare worker to start antiretroviral therapy (ARVs), a '
            'combination of medicines to treat your HIV infection? [common '
            'medicines include: combivir, truvada, atripla, nevirapine]'),
        max_length=25,
        choices=YES_NO_DWTA,
        null=True,
        blank=True,
        help_text='',
    )

    # longitudinal, YES if terminal value of first_arv  = YES
    ever_taken_arv = models.CharField(
        verbose_name=(
            'Have you ever taken any antiretroviral therapy (ARVs) for '
            'your HIV infection? [For women: Do not include treatment that '
            'you took during pregnancy to protect your baby from HIV]'),
        max_length=25,
        choices=YES_NO_DWTA,
        null=True,
        blank=False,
        help_text='',  # Q7
    )

    # longitudinal, BLANK if terminal value of first_arv  = YES
    why_no_arv = models.CharField(
        verbose_name='What was the main reason why you have not started ARVs?',
        max_length=75,
        null=True,
        blank=True,
        choices=WHY_NO_ARV_CHOICE,
        help_text='',
    )
    why_no_arv_other = OtherCharField()

    # longitudinal, DATE if terminal value date is provided
    first_arv = models.DateField(
        # Q10 populate if possible
        verbose_name=(
            'When did you first start taking antiretroviral therapy (ARVs)?'),
        validators=[date_not_future],
        null=True,
        blank=True,
        help_text=(
            'Note: If participant does not want to answer,leave blank.  '
            'If participant is unable to estimate date, leave blank.'),
    )

    on_arv = models.CharField(
        verbose_name='Are you currently taking antiretroviral therapy (ARVs)?',
        max_length=25,
        choices=YES_NO_DWTA,
        null=True,
        blank=False,
        help_text='If yes, need to answer next two questions.',   # Q11 all
    )

    regimen_currently_prescribed = models.ManyToManyField(
        Arv,
        blank=False,
        verbose_name=(
            'What antiretroviral regimen are you currently prescribed?'))

    # TODO: add rule group to required ArvHistory if NO
    first_regimen = models.CharField(
        verbose_name=(
            'Is this the first regimen that you were prescribed for your '
            'HIV infection?'),
        max_length=25,
        choices=YES_NO_REGIMEN,
        null=True,
        blank=False,
        help_text=(
            'If the participant answered NO to the question above, record '
            'prior regimen and timing of switch.'),
    )

    hospitalized_art_start = models.CharField(
        verbose_name=(
            'Were you admitted to the hospital during the ~6 months following '
            'the date on which you started ART'),
        max_length=25,
        choices=YES_NO,
        null=True,
        blank=False
    )

    hospitalized_art_start_duration = models.CharField(
        verbose_name=(
            'About how many weeks or months after starting ART were you '
            'admitted to the hospital'),
        max_length=25,
        null=True,
        validators=[
            RegexValidator(
                '^[1-9][0-9]* (weeks|months)$',
                'Invalid format. Expected \'NN weeks\' or \'NN months\'')],
        help_text=(
            'Format is phrase \'NN weeks\' or \'NN months\', '
            'e.g \'5 months\' or \'13 weeks\', etc.')
    )

    hospitalized_art_start_reason = models.ManyToManyField(
        HospitalizationReason,
        max_length=100,
        verbose_name=(
            'What was the primary reason for the hospitalization?'),
        help_text='Required if hospitalized after starting ART.'
    )

    hospitalized_art_start_reason_other = OtherCharField()

    chronic_diseases = models.ManyToManyField(
        ChronicDisease,
        verbose_name='Chronic disease related care, Specify which?',
        max_length=100,
        help_text='Required if hospitalized for chronic diseases.'
    )

    medication_toxicity = models.CharField(
        verbose_name='Medication toxicity, Specify which?',
        max_length=100,
    )

    hospitalized_reason_evidence = models.CharField(
        verbose_name=(
            'Is this the first regimen that you were prescribed for your '
            'HIV infection?'),
        max_length=25,
        choices=SOURCE_EVIDENCE,
        null=True,
    )

    hospitalized_reason_evidence_other = OtherCharField()

    clinic_receiving_from = models.CharField(
        verbose_name=(
            'Which clinic facility are you already receiving therapy from?'),
        default=None,
        null=True,
        max_length=50,
        help_text=''
    )

    next_appointment_date = models.DateField(
        verbose_name='When is your next appointment at this facility?',
        default=None,
        null=True,
        blank=True,
        help_text=''
    )

    arv_stop_date = models.DateField(
        verbose_name='When did you stop taking ARV\'s?',
        validators=[date_not_future],  # Q15
        null=True,
        blank=True,
        help_text='',
    )

    arv_stop = models.CharField(
        verbose_name='What was the main reason why you stopped taking ARVs?',
        max_length=80,
        choices=WHY_ARV_STOP_CHOICE,
        null=True,
        blank=True,
        help_text='',
    )

    arv_stop_other = OtherCharField()

    adherence_4_day = models.CharField(
        verbose_name=(
            'During the past 4 days, on how many days have you missed taking '
            'all your doses of antiretroviral therapy (ART)?'),
        max_length=25,
        choices=ADHERENCE_4DAY_CHOICE,
        null=True,
        blank=True,
        help_text='',
    )

    adherence_4_wk = models.CharField(
        verbose_name=(
            'Thinking about the past 4 weeks, on average, how would you '
            'rate your ability to take all your medications as prescribed?'),
        max_length=25,
        null=True,
        blank=True,
        choices=ADHERENCE_4WK_CHOICE,
        help_text='',
    )

    arv_evidence = models.CharField(
        verbose_name=(
            'Is there evidence [OPD card, tablets, masa number] that the '
            'participant is on therapy?'),
        choices=YES_NO,  # Q17
        null=True,
        blank=True,
        max_length=3,
    )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = 'HIV care & Adherence'
        verbose_name_plural = 'HIV care & Adherence'
