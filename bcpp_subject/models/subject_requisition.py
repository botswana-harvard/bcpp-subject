from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_dashboard.model_mixins import SearchSlugManager
from edc_lab.model_mixins import (
    RequisitionModelMixin, RequisitionStatusMixin, RequisitionIdentifierMixin)
from edc_metadata.model_mixins.updates import UpdatesRequisitionMetadataModelMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_visit_tracking.managers import (
    CrfModelManager as VisitTrackingCrfModelManager)
from edc_visit_tracking.model_mixins import (
    CrfModelMixin as VisitTrackingCrfModelMixin, PreviousVisitModelMixin)

from .model_mixins import SearchSlugModelMixin
from .requires_consent_model_mixin import RequiresConsentMixin
from .subject_visit import SubjectVisit


class Manager(VisitTrackingCrfModelManager, SearchSlugManager):
    pass


class SubjectRequisition(
        RequisitionModelMixin, RequisitionStatusMixin, RequisitionIdentifierMixin,
        VisitTrackingCrfModelMixin, OffstudyMixin,
        RequiresConsentMixin, PreviousVisitModelMixin,
        UpdatesRequisitionMetadataModelMixin, SearchSlugModelMixin,
        BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    objects = Manager()

    def get_slugs(self):
        return ([self.subject_visit.subject_identifier,
                 self.requisition_identifier,
                 self.human_requisition_identifier,
                 self.identifier_prefix]
                + self.subject_visit.household_member.get_slugs())

    class Meta(VisitTrackingCrfModelMixin.Meta, RequiresConsentMixin.Meta):
        consent_model = 'bcpp_subject.subjectconsent'
        app_label = 'bcpp_subject'
        anonymous_consent_model = 'bcpp_subject.anonymousconsent'
