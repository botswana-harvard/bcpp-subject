from django.db import models
from django.db.models.deletion import ProtectedError
from django.utils import timezone
from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_visit_schedule.model_mixins import EnrollmentModelMixin
from member.models import HouseholdMember
from survey.model_mixins import SurveyModelMixin

from .bcpp_appointment_creator import BcppAppointmentCreator, BcppAhsAppointmentCreator
from .enrollment_manager import EnrollmentManager, EnrollmentProxyModelManager
from bcpp_community.surveys import BCPP_YEAR_1, BCPP_YEAR_2, BCPP_YEAR_3
from survey.site_surveys import site_surveys


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

    appointment_creator_cls = BcppAhsAppointmentCreator

    objects = EnrollmentProxyModelManager()

    @property
    def map_area(self):
        return self.household_member.household_structure.household.plot.map_area

    def get_survey_object(self, survey=None):
        return site_surveys.get_survey_from_field_value(survey)

    def get_survey_schedule(self, household_member=None):
        return household_member.survey_schedule

    def get_household_member(self, visit_code=None):
        if visit_code == 'T1':
            try:
                return HouseholdMember.objects.get(
                    survey_schedule=f'bcpp-survey.bcpp-year-2.{self.map_area}',
                    subject_identifier=self.subject_identifier)
            except HouseholdMember.DoesNotExist:
                pass
        elif visit_code == 'T2':
            try:
                return HouseholdMember.objects.get(
                    survey_schedule=f'bcpp-survey.bcpp-year-3.{self.map_area}',
                    subject_identifier=self.subject_identifier)
            except HouseholdMember.DoesNotExist:
                pass
        return None

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
