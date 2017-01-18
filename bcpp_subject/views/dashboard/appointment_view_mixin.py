from edc_dashboard.view_mixins.subject_dashboard import AppointmentViewMixin as BaseAppointmentMixin


from member.models import HouseholdMember

from ...models import Appointment


class AppointmentViewMixin(BaseAppointmentMixin):

    def empty_appointment(self, **kwargs):
        household_member = HouseholdMember(
            household_structure=self.household_structure._original_object)
        return Appointment(household_member=household_member)
