from django.db import models
from django.db.models.deletion import PROTECT

from bcpp_labs.model_mixins import SubjectRequisitionModelMixin
from edc_base.model_mixins import BaseUuidModel
from edc_search.model_mixins import SearchSlugManager
from edc_visit_tracking.managers import CrfModelManager as VisitTrackingCrfModelManager
from edc_visit_tracking.model_mixins import CrfModelMixin as VisitTrackingCrfModelMixin

from .model_mixins import SearchSlugModelMixin
from .requires_consent_model_mixin import RequiresConsentMixin
from .subject_visit import SubjectVisit


class Manager(VisitTrackingCrfModelManager, SearchSlugManager):
    pass


class SubjectRequisition(SearchSlugModelMixin, RequiresConsentMixin,
                         SubjectRequisitionModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    objects = Manager()

    def get_search_slug_fields(self):
        fields = [
            'requisition_identifier',
            'human_readable_identifier',
            'panel_name',
            'panel_object.abbreviation',
            'identifier_prefix']
        fields.extend(
            [self.subject_visit.household_member.get_search_slug_fields()])
        return fields

    class Meta(VisitTrackingCrfModelMixin.Meta, RequiresConsentMixin.Meta):
        consent_model = 'bcpp_subject.subjectconsent'
        app_label = 'bcpp_subject'
        anonymous_consent_model = 'bcpp_subject.anonymousconsent'
