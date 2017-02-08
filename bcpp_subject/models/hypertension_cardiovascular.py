from django.db import models

from edc_constants.choices import YES_NO_NA, YES_NO

from ..choices import HEALTH_CARE_FACILITY, TOBACCO_SMOKING
from .list_models import Medication
from .model_mixins import CrfModelMixin
from edc_constants.constants import NOT_SURE, DWTA, NOT_APPLICABLE

REASONS = (
    ('afraid', 'I am afraid to know my blood pressure'),
    ('no_time', 'I do not have time'),
    ('painful', 'I was told it is painful'),
    ('not_ready', 'I am not ready'),
    (NOT_SURE, 'I am not sure why'),
    (DWTA, 'Don\'t want to answer'),
)


class HypertensionCardiovascular(CrfModelMixin):

    """Model used for getting hypertension and cardiovascular
    info.
    """

    hypertension_diagnosis = models.CharField(
        verbose_name='Have you ever been diagnosed with hypertension?',
        choices=YES_NO,
        max_length=20)

    health_care_facility = models.CharField(
        verbose_name='If yes: Health facility providing care',
        choices=HEALTH_CARE_FACILITY,
        default=NOT_APPLICABLE,
        max_length=25)

    medication_taken = models.ManyToManyField(
        Medication,
        related_name='medication_taken',
        verbose_name=(
            'Have you ever taken any of these medications? '
            'Tick all that apply'))

    medication_taken_other = models.CharField(
        verbose_name='If other please specify',
        null=True,
        blank=True,
        max_length=100)

    medication_given = models.ManyToManyField(
        Medication,
        related_name='medication_given',
        verbose_name=('If yes: Are you still being given this '
                      'medication (respond for each one ticked)'))

    medication_given_other = models.CharField(
        verbose_name='If other please specify',
        null=True,
        blank=True,
        max_length=100)

    salt_intake_counselling = models.CharField(
        verbose_name=(
            'Have you ever been counselled about salt intake '
            'by a health care worker in the past 3 years?'),
        choices=YES_NO,
        max_length=15)

    tobacco = models.CharField(
        verbose_name='Have you ever smoked tobacco products?',
        choices=YES_NO,
        max_length=20)

    tobacco_current = models.CharField(
        verbose_name='Do you currently smoke tobacco products?',
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        max_length=20)

    tobacco_counselling = models.CharField(
        verbose_name=(
            'If yes to any prior smoking of tobacco products '
            'have you been counselled about smoking cessation / not '
            'taking up smoking by a healthcare worker in the past 3 years?'),
        choices=YES_NO_NA,
        default=NOT_APPLICABLE,
        max_length=20)

    weight_history = models.CharField(
        verbose_name='Have you had your weight checked in the past 3 years?',
        choices=YES_NO_NA,
        max_length=20)

    weight_counselling = models.CharField(
        verbose_name=(
            'Have you ever been counselled about what weight you '
            'should aim for by a health care worker in the past 3 years? '),
        choices=YES_NO_NA,
        max_length=20)

    physical_activity_counselling = models.CharField(
        verbose_name=('Have you ever been counselled about the amount of '
                      'physical activity (or exercise) to maintain by a '
                      'healthcare worker in the past 3 years?'),
        choices=YES_NO_NA,
        max_length=20)

    alcohol_counselling = models.CharField(
        verbose_name=('Have you ever been counselled about correct alcohol '
                      'intake by a healthcare worker in the past 3 years?'),
        choices=YES_NO_NA,
        max_length=20)

    blood_test_for_cholesterol = models.CharField(
        verbose_name=('Have you ever had a blood test for high cholesterol '
                      'in the past 3 years?'),
        choices=YES_NO_NA,
        max_length=20)

    blood_test_for_diabetes = models.CharField(
        verbose_name=('Have you ever had blood test for sugar diabetes in '
                      'the past 3 years?'),
        choices=YES_NO_NA,
        max_length=20)

    bp = models.CharField(
        verbose_name=('As part of our questions about your health we '
                      'would like to check your blood pressure. '
                      'Are you willing to have your blood'
                      'pressure taken today?'),
        choices=YES_NO,
        max_length=5)

    bp_refused_reason = models.CharField(
        verbose_name=('If no, provide reason'),
        choices=REASONS,
        max_length=25)

    # blood pressure
    right_arm_one = models.CharField(
        verbose_name='Right Arm BP 1:',
        max_length=15,
        null=True,
        blank=True)

    left_arm_one = models.CharField(
        verbose_name='Left Arm BP 1:',
        max_length=15,
        null=True,
        blank=True)

    right_arm_two = models.CharField(
        verbose_name='Right Arm BP 2:',
        max_length=15,
        null=True,
        blank=True)

    left_arm_two = models.CharField(
        verbose_name='Left Arm BP 2:',
        max_length=15,
        null=True,
        blank=True)

    bm = models.CharField(
        verbose_name=('As part of our questions about your health we '
                      'would like to measure your '
                      'waist and hips. Are you willing to have body '
                      'measurements taken today?'),
        choices=YES_NO,
        max_length=5)

    bm_refused_reason = models.CharField(
        verbose_name=('If no, provide reason'),
        choices=REASONS,
        max_length=25)

    # waist circumference
    waist_reading_one = models.CharField(
        verbose_name='Waist circumference Measurement today (Reading 1)',
        max_length=15,
        null=True,
        blank=True)

    waist_reading_two = models.CharField(
        verbose_name='Waist circumference Measurement today (Reading 2)',
        max_length=15,
        null=True,
        blank=True)

    hip_reading_one = models.CharField(
        verbose_name='Hip circumference Measurement today (Reading 1)',
        max_length=15,
        null=True,
        blank=True)

    hip_reading_two = models.CharField(
        verbose_name='Hip circumference Measurement today (Reading 2)',
        max_length=15,
        null=True,
        blank=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = 'Hypertension and Cardiovascular Risk'
        verbose_name_plural = 'Hypertension and Cardiovascular Risk'
