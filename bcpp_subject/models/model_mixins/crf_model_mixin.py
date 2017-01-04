from django.db import models

from edc_base.model.models import UrlMixin, HistoricalRecords, BaseUuidModel
from edc_base.model.validators.date import datetime_not_future
from edc_base.utils import get_utcnow
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_visit_tracking.managers import CrfModelManager as VisitTrackingCrfModelManager
from edc_visit_tracking.model_mixins import CrfModelMixin as VisitTrackingCrfModelMixin, PreviousVisitModelMixin

from ..subject_visit import SubjectVisit
from django.db.models.deletion import PROTECT


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
                    UpdatesCrfMetadataModelMixin, UrlMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

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
        abstract = True


class CrfModelMixinNonUniqueVisit(
        VisitTrackingCrfModelMixin, OffstudyMixin,
        RequiresConsentMixin, PreviousVisitModelMixin,
        UpdatesCrfMetadataModelMixin, UrlMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

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
        abstract = True
