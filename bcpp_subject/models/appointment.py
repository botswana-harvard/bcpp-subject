from django.db import models
from edc_appointment.managers import AppointmentManager
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_appointment.model_mixins import AppointmentModelMixin

from member.models import HouseholdMember
from survey.model_mixins import SurveyModelMixin


class Appointment(AppointmentModelMixin, SurveyModelMixin, BaseUuidModel):

    # survey schedule fields are updated when the appointment
    # is created by 'create_appointments'.
    # See `extra_create_appointment_options` on the enrollment models.

    household_member = models.ForeignKey(
        HouseholdMember, on_delete=models.PROTECT)

    objects = AppointmentManager()

    history = HistoricalRecords()

    class Meta(AppointmentModelMixin.Meta):
        app_label = 'bcpp_subject'
