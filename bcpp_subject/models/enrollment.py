from uuid import uuid4

from django.db import models
from django.utils import timezone

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_base.model.models.url_mixin import UrlMixin
from edc_visit_schedule.model_mixins import EnrollmentModelMixin
from ..managers import EnrollmentManager


def get_uuid():
    return str(uuid4())


class Enrollment(EnrollmentModelMixin, CreateAppointmentsMixin, UrlMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by the SubjectConsent."""

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    survey = models.CharField(
        max_length=75)

    objects = EnrollmentManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.facility_name = 'home'
        super().save(*args, **kwargs)

    class Meta(EnrollmentModelMixin.Meta):
        app_label = 'bcpp_subject'
        consent_model = 'bcpp_subject.subjectconsent'
        visit_schedule_name = 'visit_schedule.survey_schedule'
        verbose_name = 'Enrollment'
