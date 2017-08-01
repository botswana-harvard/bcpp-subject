from django.db import models

from edc_base.model_managers import HistoricalRecords
from edc_base.model_validators import datetime_not_future
from edc_constants.choices import YES_NO

from .model_mixins import CrfModelMixin
from .subject_consent import SubjectConsent


class HicEnrollment (CrfModelMixin):

    hic_permission = models.CharField(
        verbose_name=(
            'Is it okay for the project to visit you every year for '
            'the next three years for further questions and testing?'),
        max_length=25,
        choices=YES_NO,
        help_text='If \'No\', subject is not eligible.'
    )

    permanent_resident = models.NullBooleanField(
        default=None,
        null=True,
        blank=True,
        help_text='From Residency and Mobility. Eligible if Yes.'
    )

    intend_residency = models.NullBooleanField(
        default=None,
        null=True,
        blank=True,
        help_text='From Residency and Mobility. Eligible if No.'
    )

    hiv_status_today = models.CharField(
        max_length=50,
        help_text="From Today's HIV Result. Eligible if Negative.",
    )

    dob = models.DateField(
        verbose_name="Date of birth",
        default=None,
        help_text="Format is YYYY-MM-DD. From Subject Consent.",
    )

    household_residency = models.NullBooleanField(
        default=None,
        null=True,
        blank=True,
        help_text='Is Participant a Household Member. Eligible if Yes.'
    )

    citizen_or_spouse = models.NullBooleanField(
        default=None,
        help_text=(
            'From Subject Consent. Is participant a citizen, or married to citizen '
            'with a valid marriage certificate?'),
    )

    locator_information = models.NullBooleanField(
        default=None,
        null=True,
        blank=True,
        help_text='From Subject Locator. Is the locator form filled and all '
                  'necessary contact information collected?',
    )

    consent_datetime = models.DateTimeField(
        verbose_name="Consent date and time",
        validators=[
            datetime_not_future, ],
        help_text="From Subject Consent."
    )

    history = HistoricalRecords()

    def __str__(self):
        return (f'{self.subject_visit.subject_identifier} '
                f'{self.subject_visit.report_datetime} {self.subject_visit.visit_code}')

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields')
        if not update_fields:
            first_consent = SubjectConsent.consent.first_consent(
                self.subject_identifier)
            self.dob = first_consent.dob
            self.consent_datetime = first_consent.consent_datetime
        super(HicEnrollment, self).save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Hic Enrollment"
        verbose_name_plural = "Hic Enrollment"
