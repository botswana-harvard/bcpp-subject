from bcpp_status.status_helper import StatusHelper
from django.db import models
from django.db.models.deletion import PROTECT
from bcpp_labs.model_mixins import SubjectRequisitionModelMixin
from edc_base.model_mixins import BaseUuidModel
from edc_reference.model_mixins import ReferenceModelMixin
from edc_search.model_mixins import SearchSlugManager
from edc_visit_tracking.managers import CrfModelManager as VisitTrackingCrfModelManager
from edc_visit_tracking.model_mixins import CrfModelMixin as VisitTrackingCrfModelMixin

from .requires_consent_model_mixin import RequiresConsentMixin
from .subject_visit import SubjectVisit


class Manager(VisitTrackingCrfModelManager, SearchSlugManager):
    pass


class SubjectRequisition(RequiresConsentMixin, ReferenceModelMixin,
                         SubjectRequisitionModelMixin, BaseUuidModel):

    status_helper_cls = StatusHelper

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    objects = Manager()

    def run_metadata_rules_for_crf(self):
        """Runs all the rule groups for this app label.

        Gets called in the signal.
        """
        self.status_helper_cls(visit=self.visit, update_history=True)
        self.visit.run_metadata_rules(visit=self.visit)

    class Meta(VisitTrackingCrfModelMixin.Meta, RequiresConsentMixin.Meta):
        consent_model = 'bcpp_subject.subjectconsent'
        app_label = 'bcpp_subject'
        anonymous_consent_model = 'bcpp_subject.anonymousconsent'
