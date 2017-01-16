from django.db import models
from django.utils import timezone

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_visit_schedule.model_mixins import EnrollmentModelMixin

from bcpp.surveys import ESS_SURVEY, BHS_SURVEY, AHS_SURVEY
from member.models import HouseholdMember
from survey.model_mixins import SurveyModelMixin
from survey import S

from ..exceptions import EnrollmentError
from ..managers import EnrollmentManager


class BcppEnrollmentMixin(models.Model):

    """A model used by the system. Auto-completed by the SubjectConsent."""

    ADMIN_SITE_NAME = 'bcpp_subject_admin'

    SURVEY_NAME = None

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    household_member = models.ForeignKey(HouseholdMember, on_delete=models.PROTECT)

    report_datetime = models.DateTimeField(default=timezone.now, editable=False)

    objects = EnrollmentManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.facility_name = 'home'
        s = S(self.survey)
        if s.survey_name != self.SURVEY_NAME:
            raise EnrollmentError(
                '{} enrolls to {} only. Got {}'.format(
                    self.__class__.__name__, self.SURVEY_NAME, self.survey))
        super().save(*args, **kwargs)

    @property
    def extra_create_appointment_options(self):
        return dict(
            survey=self.survey_object.field_value,
            survey_schedule=self.survey_schedule_object.field_value,
            household_member=self.household_member)

    class Meta:
        abstract = True


class EnrollmentBhs(EnrollmentModelMixin, BcppEnrollmentMixin, SurveyModelMixin,
                    CreateAppointmentsMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by the SubjectConsent."""

    SURVEY_NAME = BHS_SURVEY

    class Meta(EnrollmentModelMixin.Meta):
        app_label = 'bcpp_subject'
        consent_model = 'bcpp_subject.subjectconsent'
        visit_schedule_name = 'visit_schedule_bhs.bhs_schedule'
        verbose_name = 'Enrollment'


class EnrollmentAhs(EnrollmentModelMixin, BcppEnrollmentMixin, SurveyModelMixin,
                    CreateAppointmentsMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by the SubjectConsent."""

    SURVEY_NAME = AHS_SURVEY

    class Meta(EnrollmentModelMixin.Meta):
        app_label = 'bcpp_subject'
        consent_model = 'bcpp_subject.subjectconsent'
        visit_schedule_name = 'visit_schedule_ahs.ahs_schedule'
        verbose_name = 'Enrollment'


class EnrollmentEss(EnrollmentModelMixin, BcppEnrollmentMixin, SurveyModelMixin,
                    CreateAppointmentsMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by the SubjectConsent."""

    SURVEY_NAME = ESS_SURVEY

    class Meta(EnrollmentModelMixin.Meta):
        app_label = 'bcpp_subject'
        consent_model = 'bcpp_subject.subjectconsent'
        visit_schedule_name = 'visit_schedule_ess.ess_schedule'
        verbose_name = 'Enrollment'
