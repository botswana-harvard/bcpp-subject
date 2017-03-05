from django.db import models

from edc_base.model_managers import HistoricalRecords
from edc_base.model_validators import datetime_is_future, date_is_future
from edc_constants.constants import NOT_APPLICABLE

from ..choices import (
    REFERRAL_APPT_COMMENTS,
    REFERRAL_LETTER_YES_NO_REFUSED)

from ..referral.model_mixins import SubjectReferralModelMixin
from .model_mixins import CrfModelMixin


class SubjectReferral(SubjectReferralModelMixin, CrfModelMixin):
    """A model completed by the user to indicate a referral to care.
    """
    subject_referred = models.CharField(
        max_length=10,
        choices=REFERRAL_LETTER_YES_NO_REFUSED,
        help_text='')

    referral_appt_date = models.DateTimeField(
        verbose_name="Referral Appointment Date",
        validators=[datetime_is_future, ],
        help_text=("The calculated referral appointment date"
                   " communicated to the participant. See also "
                   "attribute 'referral_appt_comment' for when "
                   "the participant is unsure about attending "
                   "on this date."),
        null=True,
        editable=False)

    referral_appt_comment = models.CharField(
        verbose_name='Reason for not attending suggested appointment date',
        max_length=50,
        choices=REFERRAL_APPT_COMMENTS,
        default=NOT_APPLICABLE,
        help_text=('If subject is unsure about attending the suggested '
                   'appointment date, indicate the reason.'))

    scheduled_appt_date = models.DateField(
        verbose_name=("Previously scheduled clinic "
                      "appointment date in this community"),
        validators=[date_is_future, ],
        help_text=("Use the IDCC date. If subject is pregnant, "
                   "use the ANC date instead of the IDCC date."
                   "  If the subject does not have a "
                   "scheduled appointment, leave blank"),
        blank=True,
        null=True)

    comment = models.CharField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        help_text=('IMPORTANT: Do not include any names '
                   'or other personally identifying '
                   'information in this comment'))

    history = HistoricalRecords()

    def __str__(self):
        return '{0}: {1} {2} {3}'.format(self.subject_visit,
                                         self.referral_code,
                                         self.referral_appt_date,
                                         self.referral_clinic)

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
