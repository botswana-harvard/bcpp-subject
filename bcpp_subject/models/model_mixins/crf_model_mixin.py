from bcpp_status import StatusHelper
from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel, FormAsJSONModelMixin
from edc_base.model_validators import datetime_not_future
from edc_base.utils import get_utcnow
from edc_metadata.model_mixins.updates import UpdatesCrfMetadataModelMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_reference.model_mixins import ReferenceModelMixin
from edc_visit_tracking.managers import CrfModelManager as VisitTrackingCrfModelManager
from edc_visit_tracking.model_mixins import CrfModelMixin as VisitTrackingCrfModelMixin
from edc_visit_tracking.model_mixins import PreviousVisitModelMixin

from ..requires_consent_model_mixin import RequiresConsentMixin
from ..subject_visit import SubjectVisit


class CrfModelManager(VisitTrackingCrfModelManager):

    def get_by_natural_key(self, subject_identifier, visit_schedule_name,
                           schedule_name, visit_code):
        return self.get(
            subject_visit__subject_identifier=subject_identifier,
            subject_visit__visit_schedule_name=visit_schedule_name,
            subject_visit__schedule_name=schedule_name,
            subject_visit__visit_code=visit_code)


class MyUpdatesCrfMetadataModelMixin(UpdatesCrfMetadataModelMixin):

    status_helper_cls = StatusHelper

    def run_metadata_rules_for_crf(self):
        """Runs all the rule groups for this app label.

        Gets called in the signal.
        """
        self.status_helper_cls(visit=self.visit, update_history=True)
        self.visit.run_metadata_rules(visit=self.visit)

    class Meta:
        abstract = True


class CrfModelMixin(VisitTrackingCrfModelMixin, OffstudyMixin,
                    RequiresConsentMixin, PreviousVisitModelMixin,
                    MyUpdatesCrfMetadataModelMixin,
                    FormAsJSONModelMixin, ReferenceModelMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`).
    """

    subject_visit = models.OneToOneField(SubjectVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_future, datetime_not_before_study_start],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    objects = CrfModelManager()

    history = HistoricalRecords()

    def natural_key(self):
        return self.subject_visit.natural_key()
    natural_key.dependencies = ['bcpp_subject.subjectvisit']

    class Meta(VisitTrackingCrfModelMixin.Meta, RequiresConsentMixin.Meta):
        consent_model = 'bcpp_subject.subjectconsent'
        anonymous_consent_model = 'bcpp_subject.anonymousconsent'
        abstract = True


# class CrfModelMixinNonUniqueVisit(
#         VisitTrackingCrfModelMixin, OffstudyMixin,
#         RequiresConsentMixin, PreviousVisitModelMixin,
#         UpdatesCrfMetadataModelMixin, BaseUuidModel):
#
#     """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """
#
#     subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)
#
#     report_datetime = models.DateTimeField(
#         verbose_name="Report Date",
#         validators=[
#             datetime_not_future, ],
#         default=get_utcnow,
#         help_text=('If reporting today, use today\'s date/time, otherwise use '
#                    'the date/time this information was reported.'))
#
#     objects = CrfModelManager()
#
#     history = HistoricalRecords()
#
#     def natural_key(self):
#         return self.subject_visit.natural_key()
#     natural_key.dependencies = ['bcpp_subject.subjectvisit']
#
#     class Meta(VisitTrackingCrfModelMixin.Meta, RequiresConsentMixin.Meta):
#         consent_model = 'bcpp_subject.subjectconsent'
#         anonymous_consent_model = 'bcpp_subject.anonymousconsent'
#         abstract = True
