from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_lab.model_mixins import RequisitionModelMixin
from edc_metadata.model_mixins.updates import UpdatesRequisitionMetadataModelMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_visit_tracking.managers import (
    CrfModelManager as VisitTrackingCrfModelManager)
from edc_visit_tracking.model_mixins import (
    CrfModelMixin as VisitTrackingCrfModelMixin, PreviousVisitModelMixin)

from .subject_visit import SubjectVisit
from .requires_consent_model_mixin import RequiresConsentMixin


class SubjectRequisition(
        RequisitionModelMixin, VisitTrackingCrfModelMixin, OffstudyMixin,
        RequiresConsentMixin, PreviousVisitModelMixin,
        UpdatesRequisitionMetadataModelMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    subject_visit = models.ForeignKey(SubjectVisit)

    objects = VisitTrackingCrfModelManager()

    class Meta(VisitTrackingCrfModelMixin.Meta, RequiresConsentMixin.Meta):
        consent_model = 'bcpp_subject.subjectconsent'
        app_label = 'bcpp_subject'
        anonymous_consent_model = 'bcpp_subject.anonymousconsent'
