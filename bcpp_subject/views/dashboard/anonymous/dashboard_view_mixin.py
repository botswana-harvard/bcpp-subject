from edc_dashboard.view_mixins import (
    ShowHideViewMixin, SubjectIdentifierViewMixin, VisitScheduleViewMixin, MetaDataViewMixin)

from household.views.mixins import HouseholdStructureViewMixin
from member.views import HouseholdMemberViewMixin

from ..consent_view_mixin import ConsentViewMixin
from ..appointment_view_mixin import AppointmentViewMixin

from ..enrollment_forms_view_mixin import EnrollmentFormsViewMixin

from .household_view_mixin import HouseholdViewMixin


class DashboardViewMixin(
        EnrollmentFormsViewMixin,
        HouseholdViewMixin, HouseholdStructureViewMixin, HouseholdMemberViewMixin,
        ConsentViewMixin, VisitScheduleViewMixin,
        AppointmentViewMixin, MetaDataViewMixin, ShowHideViewMixin,
        SubjectIdentifierViewMixin):
    pass
