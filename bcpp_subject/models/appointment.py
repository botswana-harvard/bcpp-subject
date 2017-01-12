from edc_appointment.managers import AppointmentManager
from edc_base.model.models import HistoricalRecords, BaseUuidModel, UrlMixin
from edc_appointment.model_mixins import AppointmentModelMixin
from survey.model_mixins import SurveyModelMixin


class Appointment(AppointmentModelMixin, SurveyModelMixin, UrlMixin, BaseUuidModel):

    objects = AppointmentManager()

    history = HistoricalRecords()

    class Meta(AppointmentModelMixin.Meta):
        app_label = 'bcpp_subject'
