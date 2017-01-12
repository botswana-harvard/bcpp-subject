from uuid import uuid4

from django.db import models
from django.utils import timezone

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_base.model.models.url_mixin import UrlMixin
from edc_visit_schedule.model_mixins import EnrollmentModelMixin

from bcpp.surveys import ESS_SURVEY

from ..managers import EnrollmentManager

from survey.model_mixins import SurveyModelMixin

from ..exceptions import EnrollmentError


def get_uuid():
    return str(uuid4())


class EnrollmentEss(EnrollmentModelMixin, SurveyModelMixin, CreateAppointmentsMixin, UrlMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by the SubjectConsent."""

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    objects = EnrollmentManager()

    history = HistoricalRecords()
edc_appointment
    def save(self, *args, **kwargs):
        self.facility_name = 'home'
        if self.survey != ESS_SURVEY:
            raise EnrollmentError(
                '{} enrolls to ESS only. Got {}'.format(self.__class__.__name__, self.survey))
        super().save(*args, **kwargs)

    @property
    def extra_create_appointment_options(self):
        return dict(
            survey=self.survey_object.name,
            survey_schedule=self.survey_schedule_object.field_name)

    class Meta(EnrollmentModelMixin.Meta):
        app_label = 'bcpp_subject'
        consent_model = 'bcpp_subject.subjectconsent'
        visit_schedule_name = 'visit_schedule_ess.ess_schedule'
        verbose_name = 'Enrollment'
