from django.db import models

from edc_base.model.models import UrlMixin, BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_lab.model_mixins import RequisitionModelMixin
from edc_metadata.model_mixins import UpdatesRequisitionMetadataModelMixin
from edc_offstudy.model_mixins import OffstudyMixin
from edc_visit_tracking.managers import CrfModelManager as VisitTrackingCrfModelManager
from edc_visit_tracking.model_mixins import CrfModelMixin as VisitTrackingCrfModelMixin, PreviousVisitModelMixin

from bcpp_subject.models.subject_visit import SubjectVisit


class SubjectRequisition(
        RequisitionModelMixin, VisitTrackingCrfModelMixin, OffstudyMixin, RequiresConsentMixin, PreviousVisitModelMixin,
        UpdatesRequisitionMetadataModelMixin, UrlMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    objects = VisitTrackingCrfModelManager()

    class Meta(VisitTrackingCrfModelMixin.Meta):
        consent_model = 'bcpp_subject.subjectconsent'
        app_label = 'bcpp_subject'
