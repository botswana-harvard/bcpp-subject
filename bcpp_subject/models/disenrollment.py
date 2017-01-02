from edc_base.model.models import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentMixin
from edc_visit_schedule.model_mixins import DisenrollmentModelMixin

from ..managers import DisenrollmentManager


class Disenrollment(DisenrollmentModelMixin, RequiresConsentMixin, BaseUuidModel):

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    objects = DisenrollmentManager()

    class Meta(DisenrollmentModelMixin.Meta):
        visit_schedule_name = 'visit_schedule'
        consent_model = 'bcpp_subject.subjectconsent'
        app_label = 'bcpp_subject'
