from django.db import models
from django.utils import timezone

from edc_appointment.model_mixins import CreateAppointmentsMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_visit_schedule.model_mixins import EnrollmentModelMixin

from bcpp.surveys import (
    BHS_SURVEY, AHS_SURVEY, ESS_SURVEY, ANONYMOUS_SURVEY, BCPP_YEAR_3)
from member.models import HouseholdMember
from survey.model_mixins import SurveyModelMixin
from survey import S

from ..exceptions import EnrollmentError
from ..managers import EnrollmentManager as BaseEnrollmentManager
from survey.site_surveys import site_surveys


class EnrollmentManager(BaseEnrollmentManager):

    def enroll_to_next_survey(self,
                              consent_identifier=None,
                              subject_identifier=None,
                              household_member=None,
                              report_datetime=None,
                              save=None):
        """Returns a survey object, or None, which represents the
        next survey in the survey schedule that the subject has not yet
        enrolled into.
        """
        next_survey_object = None
        save = True if save is None else save

        # do you have any previous surveys?
        last_enrollment = self.filter(
            subject_identifier=subject_identifier).order_by(
                '-report_datetime').last()
        if last_enrollment:
            # get last survey object
            last_survey_object = last_enrollment.survey_object
            # build survey object for next using current survey_schedule_object
            if last_survey_object.next:
                survey_field_value = S(
                    household_member.survey_schedule_object.field_value,
                    survey_name=last_survey_object.next.name).survey_field_value
                next_survey_object = site_surveys.get_survey(
                    survey_field_value, current=False)
        else:
            next_survey_object = self.get_first_survey(
                household_member.survey_schedule_object)

        if next_survey_object:
            try:
                enrollment = self.get(
                    survey=next_survey_object.field_value,
                    subject_identifier=subject_identifier)
            except Enrollment.DoesNotExist:
                model = self.get_enrollment_model_class(next_survey_object)
                enrollment = model(
                    consent_identifier=consent_identifier,
                    subject_identifier=subject_identifier,
                    household_member=household_member,
                    report_datetime=report_datetime,
                    survey=next_survey_object.field_value)
                if save:
                    enrollment.save()
        else:
            raise EnrollmentError(
                'No surveys in this survey schedule left to enroll. '
                'Got {}.'.format(
                    household_member.survey_schedule_object.field_value))
        return next_survey_object

    def get_first_survey(self, survey_schedule_object=None):
        """Returns a survey object.

        This is the first ever survey

        Note special case for YEAR 3 where first survey is ESS"""
        if survey_schedule_object.name == BCPP_YEAR_3:
            return survey_schedule_object.get_survey(name=ESS_SURVEY)
        else:
            return survey_schedule_object.surveys[0]

    def get_enrollment_model_class(self, survey_object):
        """Returns the proxy model class for the given survey name."""
        if survey_object.name == BHS_SURVEY:
            return EnrollmentBhs
        elif survey_object.name == AHS_SURVEY:
            return EnrollmentAhs
        elif survey_object.name == ESS_SURVEY:
            return EnrollmentEss
        elif survey_object.name == ANONYMOUS_SURVEY:
            return EnrollmentAno


class EnrollmentProxyModelManager(BaseEnrollmentManager):

    def get_queryset(self):
        qs = super().get_queryset()
        visit_schedule_name = qs.model._meta.visit_schedule_name.split('.')[0]
        schedule_name = qs.model._meta.visit_schedule_name.split('.')[1]
        return qs.filter(
            visit_schedule_name=visit_schedule_name,
            schedule_name=schedule_name,
        )


class Enrollment(EnrollmentModelMixin, SurveyModelMixin,
                 CreateAppointmentsMixin, BaseUuidModel):

    """A model used by the system. Auto-completed by the
    SubjectConsent.
    """

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

    objects = EnrollmentProxyModelManager()

    class Meta:
        proxy = True
        visit_schedule_name = 'visit_schedule_bhs.bhs_schedule'


class EnrollmentAhs(Enrollment):

    objects = EnrollmentProxyModelManager()

    class Meta:
        proxy = True
        visit_schedule_name = 'visit_schedule_ahs.ahs_schedule'


class EnrollmentEss(Enrollment):

    objects = EnrollmentProxyModelManager()

    class Meta:
        proxy = True
        visit_schedule_name = 'visit_schedule_ess.ess_schedule'


class EnrollmentAno(Enrollment):

    objects = EnrollmentProxyModelManager()

    class Meta:
        proxy = True
        visit_schedule_name = 'visit_schedule_ano.ano_schedule'
