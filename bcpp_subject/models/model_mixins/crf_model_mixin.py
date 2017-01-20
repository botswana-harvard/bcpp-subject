from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models import options

from edc_base.model.models import HistoricalRecords, BaseUuidModel
from edc_base.model.validators.date import datetime_not_future
from edc_base.utils import get_utcnow
from edc_consent.model_mixins import RequiresConsentMixin as BaseRequiresConsentMixin
from edc_consent.site_consents import site_consents
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_visit_tracking.managers import CrfModelManager as VisitTrackingCrfModelManager
from edc_visit_tracking.model_mixins import CrfModelMixin as VisitTrackingCrfModelMixin, PreviousVisitModelMixin

from ..subject_visit import SubjectVisit

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('anonymous_consent_model',)


class RequiresConsentMixin(BaseRequiresConsentMixin):

    def get_consent_object(self):
        if self.household_member.anonymous:
            consent_object = site_consents.get_consent(
                consent_model=self._meta.anonymous_consent_model,
                report_datetime=self.report_datetime)
        else:
            consent_object = site_consents.get_consent(
                consent_model=self._meta.consent_model,
                report_datetime=self.report_datetime)
        return consent_object

    class Meta:
        abstract = True
        consent_model = None
        anonymous_consent_model = None


class CrfModelManager(VisitTrackingCrfModelManager):

    def get_by_natural_key(self, subject_identifier, visit_schedule_name, schedule_name, visit_code):
        return self.get(
            subject_visit__subject_identifier=subject_identifier,
            subject_visit__visit_schedule_name=visit_schedule_name,
            subject_visit__schedule_name=schedule_name,
            subject_visit__visit_code=visit_code
        )


class CrfModelMixin(VisitTrackingCrfModelMixin, OffstudyMixin,
                    RequiresConsentMixin, PreviousVisitModelMixin,
                    UpdatesCrfMetadataModelMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    subject_visit = models.OneToOneField(SubjectVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_future, ],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    objects = CrfModelManager()

    history = HistoricalRecords()

    def natural_key(self):
        return self.subject_visit.natural_key()
    natural_key.dependencies = ['bcpp_subject.subjectvisit']

    class Meta(VisitTrackingCrfModelMixin.Meta):
        consent_model = 'bcpp_subject.subjectconsent'
        anonymous_consent_model = 'bcpp_subject.anonymousconsent'
        abstract = True


class CrfModelMixinNonUniqueVisit(
        VisitTrackingCrfModelMixin, OffstudyMixin,
        RequiresConsentMixin, PreviousVisitModelMixin,
        UpdatesCrfMetadataModelMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_future, ],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    objects = CrfModelManager()

    history = HistoricalRecords()

    def natural_key(self):
        return self.subject_visit.natural_key()
    natural_key.dependencies = ['bcpp_subject.subjectvisit']

    class Meta(VisitTrackingCrfModelMixin.Meta):
        consent_model = 'bcpp_subject.subjectconsent'
        anonymous_consent_model = 'bcpp_subject.anonymousconsent'
        abstract = True
