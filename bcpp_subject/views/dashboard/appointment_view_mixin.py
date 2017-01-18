from edc_dashboard.view_mixins.subject_dashboard import AppointmentViewMixin as BaseAppointmentMixin


from member.models import HouseholdMember

from ...models import Appointment

from ..wrappers import AppointmentModelWrapper


class AppointmentViewMixin(BaseAppointmentMixin):

    appointment_model_wrapper_class = AppointmentModelWrapper

    def empty_appointment(self, **kwargs):
        household_member = HouseholdMember(
            household_structure=self.household_structure._original_object)
        return Appointment(household_member=household_member)
