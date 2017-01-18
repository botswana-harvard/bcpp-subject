from edc_dashboard.view_mixins import (
    ShowHideViewMixin, SubjectIdentifierViewMixin, VisitScheduleViewMixin, MetaDataViewMixin)

from household.views import HouseholdStructureViewMixin
from member.views import HouseholdMemberViewMixin

from .consent_view_mixin import ConsentViewMixin
from .appointment_view_mixin import AppointmentViewMixin


class SubjectDashboardViewMixin(
        ShowHideViewMixin, SubjectIdentifierViewMixin, HouseholdStructureViewMixin,
        HouseholdMemberViewMixin, ConsentViewMixin, VisitScheduleViewMixin,
        AppointmentViewMixin, MetaDataViewMixin):
    pass
