from django.db import models
from django.db.models.deletion import PROTECT

from edc_base.model_mixins import BaseUuidModel
from edc_dashboard.model_mixins import SearchSlugManager
from edc_lab.model_mixins.requisition import (
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
from edc_map.site_mappers import site_mappers


class Manager(VisitTrackingCrfModelManager, SearchSlugManager):
    pass


class SubjectRequisition(
        RequisitionModelMixin, RequisitionStatusMixin, RequisitionIdentifierMixin,
        VisitTrackingCrfModelMixin, OffstudyMixin,
        RequiresConsentMixin, PreviousVisitModelMixin,
        UpdatesRequisitionMetadataModelMixin, SearchSlugModelMixin,
        BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    objects = Manager()

    def save(self, *args, **kwargs):
        self.study_site = site_mappers.current_map_code
        self.study_site_name = site_mappers.current_map_area
        super().save(*args, **kwargs)

    def get_slugs(self):
        return ([self.subject_visit.subject_identifier,
                 self.requisition_identifier,
                 self.human_readable_identifier,
                 self.identifier_prefix]
                + self.subject_visit.household_member.get_slugs())

    class Meta(VisitTrackingCrfModelMixin.Meta, RequiresConsentMixin.Meta):
        consent_model = 'bcpp_subject.subjectconsent'
        app_label = 'bcpp_subject'
        anonymous_consent_model = 'bcpp_subject.anonymousconsent'
