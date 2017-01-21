from edc_dashboard.view_mixins import (
    ShowHideViewMixin, SubjectIdentifierViewMixin, VisitScheduleViewMixin, MetaDataViewMixin)

from household.views.mixins import HouseholdStructureViewMixin
from member.views import HouseholdMemberViewMixin

from ..consent_view_mixin import ConsentViewMixin
from ..appointment_view_mixin import AppointmentViewMixin

from .household_view_mixin import HouseholdViewMixin


class DashboardViewMixin(
        ShowHideViewMixin, SubjectIdentifierViewMixin,
        HouseholdViewMixin, HouseholdStructureViewMixin, HouseholdMemberViewMixin,
        ConsentViewMixin, VisitScheduleViewMixin,
        AppointmentViewMixin, MetaDataViewMixin):
    pass
