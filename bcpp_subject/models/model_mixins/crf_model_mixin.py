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


class CrfModelManager(VisitTrackingCrfModelManager):

    def get_by_natural_key(self, subject_visit):
        return self.get(**{self.model.visit_model_attr(): subject_visit})


class CrfModelMixin(VisitTrackingCrfModelMixin, OffstudyMixin,
                    RequiresConsentMixin, PreviousVisitModelMixin,
                    UpdatesCrfMetadataModelMixin, UrlMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    subject_visit = models.OneToOneField(SubjectVisit)

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
