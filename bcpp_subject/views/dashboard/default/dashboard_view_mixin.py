from edc_dashboard.view_mixins import (
    ShowHideViewMixin, SubjectIdentifierViewMixin,
    MetaDataViewMixin)

from household.views.mixins import (
    HouseholdViewMixin, HouseholdStructureViewMixin,
    HouseholdLogEntryViewMixin)
from member.views import HouseholdMemberViewMixin

from ..appointment_view_mixin import AppointmentViewMixin
from ..consent_view_mixin import ConsentViewMixin
from ..visit_schedule_view_mixin import VisitScheduleViewMixin
from .subject_locator_view_mixin import SubjectLocatorViewMixin


class DashboardViewMixin(
        SubjectIdentifierViewMixin, AppointmentViewMixin,
        MetaDataViewMixin, VisitScheduleViewMixin,
        SubjectLocatorViewMixin,
        HouseholdViewMixin, HouseholdStructureViewMixin,
        HouseholdLogEntryViewMixin, HouseholdMemberViewMixin,
        ConsentViewMixin, ShowHideViewMixin):
    pass
