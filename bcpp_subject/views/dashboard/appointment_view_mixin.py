from edc_dashboard.view_mixins.subject_dashboard import (
    AppointmentViewMixin as BaseAppointmentMixin)

from member.models import HouseholdMember

from ...models import Appointment
from ..wrappers import AppointmentModelWrapper


class AppointmentViewMixin(BaseAppointmentMixin):

    appointment_model_wrapper_class = AppointmentModelWrapper

    @property
    def appointments(self):
        appointments = super().appointments
        return (
            obj for obj in appointments
            if obj.survey_schedule_object.field_value
            == self.survey_schedule_object.field_value)

    def empty_appointment(self, **kwargs):
        household_member = HouseholdMember(
            household_structure=self.household_structure._original_object)
        return Appointment(household_member=household_member)
