from django.db import models
from django.db.models.deletion import ProtectedError
from django.utils import timezone
from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_visit_schedule.model_mixins import EnrollmentModelMixin
from member.models import HouseholdMember
from survey.model_mixins import SurveyModelMixin

from .bcpp_appointment_creator import BcppAppointmentCreator
from .enrollment_manager import EnrollmentManager, EnrollmentProxyModelManager


class Enrollment(EnrollmentModelMixin, SurveyModelMixin,
                 CreateAppointmentsMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by the
    Subject and Anonymous Consents.
    """

    appointment_creator_cls = BcppAppointmentCreator

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    household_member = models.ForeignKey(
        HouseholdMember,
        on_delete=models.PROTECT)

    consent_identifier = models.UUIDField()

    report_datetime = models.DateTimeField(
        default=timezone.now,
        editable=False)

    objects = EnrollmentManager()

    history = HistoricalRecords()

    def __str__(self):
        return '{} {} survey={}'.format(
            self.subject_identifier,
            self.schedule_name,
            self.survey_object.name)

    def save(self, *args, **kwargs):
        self.facility_name = 'home'
        self.survey_schedule = (
            self.household_member.survey_schedule_object.field_value)
        super().save(*args, **kwargs)

    @property
    def visit_code(self):
        return 'T0'

    def delete_unused_appointments(self):
        appointments = self.appointment_model.objects.filter(
            survey=self.survey_object.field_value,
            survey_schedule=self.survey_schedule_object.field_value,
            household_member=self.household_member)
        for appointment in appointments:
            try:
                appointment.delete()
            except ProtectedError:
                pass
        return None

    class Meta(EnrollmentModelMixin.Meta):
        app_label = 'bcpp_subject'
        consent_model = 'bcpp_subject.subjectconsent'
        verbose_name = 'Enrollment'


class EnrollmentBhs(Enrollment):

    objects = EnrollmentProxyModelManager()

    class Meta:
        proxy = True
        visit_schedule_name = 'visit_schedule_bhs.bhs_schedule'
        verbose_name = 'Enrollment Bhs'
        verbose_name_plural = 'Enrollment Bhs'


class EnrollmentAhs(Enrollment):

    objects = EnrollmentProxyModelManager()

    class Meta:
        proxy = True
        visit_schedule_name = 'visit_schedule_ahs.ahs_schedule'
        verbose_name = 'Enrollment Ahs'
        verbose_name_plural = 'Enrollment Ahs'


class EnrollmentEss(Enrollment):

    objects = EnrollmentProxyModelManager()

    class Meta:
        proxy = True
        verbose_name = 'Enrollment Ess'
        verbose_name_plural = 'Enrollment Ess'
        visit_schedule_name = 'visit_schedule_ess.ess_schedule'


class EnrollmentAno(Enrollment):

    objects = EnrollmentProxyModelManager()

    class Meta:
        proxy = True
        verbose_name = 'Enrollment Anonymous'
        verbose_name_plural = 'Enrollment Anonymous'
        visit_schedule_name = 'visit_schedule_ano.ano_schedule'
