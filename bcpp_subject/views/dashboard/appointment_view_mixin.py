from edc_appointment.constants import NEW_APPT
from edc_dashboard.view_mixins import AppointmentViewMixin as BaseAppointmentMixin
from member.models import HouseholdMember

from ...models import Appointment
from ..wrappers import AppointmentModelWrapper


class AppointmentViewMixin(BaseAppointmentMixin):

    appointment_model_wrapper_class = AppointmentModelWrapper

    @property
    def appointments(self):
        appointments = super().appointments
        for appointment in appointments:
            if appointment.appt_status == NEW_APPT:
                print(self.household_member, appointment)
                appointment.household_member = self.household_member
                appointment.save()
        return Appointment.objects.filter(
            household_member=self.household_member)

#     @property
#     def appointments(self):
#         appointments = super().appointments
#         print(appointments)
#         return [
#             obj for obj in appointments
#             if obj.survey_schedule_object.field_value
#             == self.survey_schedule_object.field_value]

    def empty_appointment(self, **kwargs):
        household_member = HouseholdMember(
            household_structure=self.household_structure._original_object)
        return Appointment(household_member=household_member)
