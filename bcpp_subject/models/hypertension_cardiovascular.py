from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_constants.choices import YES_NO, YES

from ..choices import HEALTH_CARE_FACILITY, TOBACCO_SMOKING
from .list_models import MedicationGiven, MedicationTaken


class HypertensionCardiovascular(BaseUuidModel):

    """Model used for getting hypertension and cardiovascular info"""

    may_take_blood_pressure = models.CharField(
        verbose_name='As part of our questions about your health we would like to check your\
        blood pressure and measure your waist and hips. Are you willing to have your blood \
        pressure and body measurements taken today?',
        choices=YES_NO,
        max_length=5,
        default='Yes')

    hypertension_diagnosis = models.CharField(
        verbose_name='Have you ever been diagnosed with hypertension?',
        choices=YES_NO,
        null=True,
        default='Yes',
        max_length=5)

    medications_taken = models.ManyToManyField(
        MedicationTaken,
        null=True)

    if_other = models.CharField(
        verbose_name='If other please specify',
        null=True,
        max_length=100)

    medication_still_given = models.ManyToManyField(
        MedicationGiven,
        null=True)

    if_other_given_medication_given = models.CharField(
        verbose_name='If other please specify',
        null=True,
        max_length=100)

    health_care_facility = models.CharField(
        verbose_name='If yes: Health facility providing care',
        choices=HEALTH_CARE_FACILITY,
        null=True,
        max_length=50,
        default='clinic')

    salt_intake_counselling = models.CharField(
        verbose_name='Have you ever been counselled about salt intake by a health care worker in the past 3 years?',
        choices=YES_NO,
        null=True,
        max_length=5,
        default='Yes')

    tobacco_smoking = models.CharField(
        verbose_name='Have you ever smoked tobacco products?',
        choices=TOBACCO_SMOKING,
        null=True,
        max_length=10,
        default='never')

    tobacco_counselling = models.CharField(
        verbose_name='If yes to any prior smoking of tobacco products, have you been counselled about smoking \
        cessation / not taking up smoking by a healthcare worker in the past 3 years?',
        choices=YES_NO,
        null=True,
        max_length=5,
        default=YES)

    weight_counselling = models.CharField(
        verbose_name='Have you ever been counselled about what weight you should aim for by a health care worker \
        in the past 3 years?',
        choices=YES_NO,
        null=True,
        max_length=5,
        default='Yes')

    physical_activity_counselling = models.CharField(
        verbose_name='Have you ever been counselled about the amount of physical activity (or exercise) to \
        maintain by a healthcare worker in the past 3 years?',
        choices=YES_NO,
        null=True,
        max_length=5,
        default='Yes')

    alcohol_counselling = models.CharField(
        verbose_name='Have you ever been counselled about correct alcohol intake by a healthcare worker in \
        the past 3 years?',
        choices=YES_NO,
        null=True,
        max_length=5,
        default='Yes')

    blood_test_for_cholesterol = models.CharField(
        verbose_name='Have you ever had a blood test for high cholesterol in the past 3 years?',
        choices=YES_NO,
        null=True,
        max_length=5,
        default='Yes')

    blood_test_for_diabetes = models.CharField(
        verbose_name='Have you ever had blood test for sugar diabetes in the past 3 years?',
        choices=YES_NO,
        null=True,
        max_length=5,
        default='Yes')

    history = HistoricalRecords()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = 'Hypertension and Cardiovascular Risk'
        verbose_name_plural = 'Hypertension and Cardiovascular Risk'


class BPMeasurement(models.Model):

    bp_measurement = models.OneToOneField(
        HypertensionCardiovascular,
        on_delete=models.CASCADE,
        null=True,)

    time_zero = models.CharField(
        verbose_name='BP at time 0:',
        max_length=15)

    right_arm_one = models.CharField(
        verbose_name='Right Arm BP 1:',
        max_length=15)

    left_arm_one = models.CharField(
        verbose_name='Left Arm BP 1:',
        max_length=15)

    right_arm_two = models.CharField(
        verbose_name='Right Arm BP 2:',
        max_length=15)

    left_arm_two = models.CharField(
        verbose_name='Left Arm BP 2:',
        max_length=15)

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = 'Blood Pressure Measurements'
        verbose_name_plural = 'Blood Pressure Measurements'


class WaistCircumferenceMeasurement(models.Model):

    waist_circumference_measurement = models.OneToOneField(
        HypertensionCardiovascular,
        on_delete=models.CASCADE,
        null=True)

    waist_reading_one = models.CharField(
        verbose_name='Waist circumference Measurement today (Reading 1)',
        max_length=15)

    waist_reading_two = models.CharField(
        verbose_name='Waist circumference Measurement today (Reading 2)',
        max_length=15)

    hip_reading_one = models.CharField(
        verbose_name='Hip circumference Measurement today (Reading 1)',
        max_length=15)

    hip_reading_two = models.CharField(
        verbose_name='Hip circumference Measurement today (Reading 2)',
        max_length=15)

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = 'Waist and Hip Measurements'
        verbose_name_plural = 'Waist and Hip Measurements'
