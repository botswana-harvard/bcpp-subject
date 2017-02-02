from edc_dashboard.view_mixins import (
    ShowHideViewMixin, SubjectIdentifierViewMixin,
    MetaDataViewMixin)

from household.views.mixins import (
    HouseholdStructureViewMixin, HouseholdLogEntryViewMixin)
from member.views import HouseholdMemberViewMixin

from ..consent_view_mixin import ConsentViewMixin
from ..appointment_view_mixin import AppointmentViewMixin
from ..visit_schedule_view_mixin import VisitScheduleViewMixin
from .household_view_mixin import HouseholdViewMixin


class DashboardViewMixin(
        SubjectIdentifierViewMixin, AppointmentViewMixin, MetaDataViewMixin,
        VisitScheduleViewMixin,
        HouseholdLogEntryViewMixin, HouseholdViewMixin,
        HouseholdStructureViewMixin, HouseholdMemberViewMixin,
        ConsentViewMixin, ShowHideViewMixin):
    pass
