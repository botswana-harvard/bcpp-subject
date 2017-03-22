from django.db import models
from edc_appointment.managers import AppointmentManager
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_appointment.model_mixins import AppointmentModelMixin

from member.models import HouseholdMember
from survey.model_mixins import SurveyModelMixin
from survey.site_surveys import site_surveys
from survey.sparser import S


class Appointment(AppointmentModelMixin, SurveyModelMixin, BaseUuidModel):

    # survey schedule fields are updated when the appointment
    # is created by 'create_appointments'.
    # See `extra_create_appointment_options` on the enrollment models.

    household_member = models.ForeignKey(
        HouseholdMember, on_delete=models.PROTECT)

    objects = AppointmentManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        """Update survey schedule and survey to show same survey year as
        household member.
        """
        self.survey_schedule = self.household_member.survey_schedule
        survey_name = site_surveys.get_survey_from_field_value(
            self.survey).name
        self.survey = S(self.survey_schedule_object.field_value,
                        survey_name=survey_name).survey_field_value
        super().save(*args, **kwargs)

    class Meta(AppointmentModelMixin.Meta):
        app_label = 'bcpp_subject'
