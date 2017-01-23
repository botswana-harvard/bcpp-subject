from django.db import models
from django.utils import timezone

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_visit_schedule.model_mixins import EnrollmentModelMixin

from bcpp.surveys import (
    BHS_SURVEY, AHS_SURVEY, ESS_SURVEY, ANONYMOUS_SURVEY, BCPP_YEAR_3)
from member.models import HouseholdMember
from survey.model_mixins import SurveyModelMixin

from ..exceptions import EnrollmentError
from ..managers import EnrollmentManager as BaseEnrollmentManager


class EnrollmentManager(BaseEnrollmentManager):

    def enroll_to_next_survey(self,
                              consent_identifier=None,
                              subject_identifier=None,
                              household_member=None,
                              report_datetime=None,
                              save=None):
        """Returns a survey object, or None, which represents the
        next survey in the survey schedule that the subject has not yet
        enrolled into."""
        save = True if save is None else save
        survey_schedule_object = household_member.survey_schedule_object
        defaults = dict(
            subject_identifier=subject_identifier,
            survey_schedule=survey_schedule_object.field_value)
        # loop through looking for a survey not yet enrolled to.
        existing = None  # existing enrollment instance
        for survey in survey_schedule_object.surveys:
            try:
                existing = self.get(
                    survey=survey.field_value,
                    **defaults)
            except Enrollment.DoesNotExist:
                break
            else:
                continue
        if existing:
            survey = existing.survey.next
        else:
            survey = self.get_first_survey(
                subject_identifier=subject_identifier,
                survey_schedule_object=survey_schedule_object)
        if survey:
            model = self.get_enrollment_model_class(survey)
            enrollment = model(
                consent_identifier=consent_identifier,
                subject_identifier=subject_identifier,
                household_member=household_member,
                report_datetime=report_datetime,
                survey=survey.field_value)
            if save:
                enrollment.save()
        else:
            raise EnrollmentError(
                'No surveys in this schedule left to enroll.')
        return survey

    def get_first_survey(self, subject_identifier=None,
                         survey_schedule_object=None):
        """Returns a survey object.

        This is the first ever survey

        Note special case for YEAR 3 where first survey is ESS"""
        if survey_schedule_object.name == BCPP_YEAR_3:
            return survey_schedule_object.get_survey(name=ESS_SURVEY)
        else:
            return survey_schedule_object.surveys[0]

    def get_enrollment_model_class(self, survey):
        """Returns the proxy model class for the given survey name."""
        if survey.name == BHS_SURVEY:
            return EnrollmentBhs
        elif survey.name == AHS_SURVEY:
            return EnrollmentAhs
        elif survey.name == ESS_SURVEY:
            return EnrollmentEss
        elif survey.name == ANONYMOUS_SURVEY:
            return EnrollmentAno


class Enrollment(EnrollmentModelMixin, SurveyModelMixin,
                 CreateAppointmentsMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by the SubjectConsent."""

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

    def save(self, *args, **kwargs):
        self.facility_name = 'home'
        self.survey_schedule = (
            self.household_member.survey_schedule_object.field_value)
        super().save(*args, **kwargs)

    @property
    def extra_create_appointment_options(self):
        return dict(
            survey=self.survey_object.field_value,
            survey_schedule=self.survey_schedule_object.field_value,
            household_member=self.household_member)

    class Meta(EnrollmentModelMixin.Meta):
        app_label = 'bcpp_subject'
        consent_model = 'bcpp_subject.subjectconsent'
        verbose_name = 'Enrollment'


class EnrollmentBhs(Enrollment):
    class Meta:
        proxy = True
        visit_schedule_name = 'visit_schedule_bhs.bhs_schedule'


class EnrollmentAhs(Enrollment):
    class Meta:
        proxy = True
        visit_schedule_name = 'visit_schedule_ahs.ahs_schedule'


class EnrollmentEss(Enrollment):
    class Meta:
        proxy = True
        visit_schedule_name = 'visit_schedule_ess.ess_schedule'


class EnrollmentAno(Enrollment):
    class Meta:
        proxy = True
        visit_schedule_name = 'visit_schedule_ano.ano_schedule'
