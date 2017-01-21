from edc_dashboard.view_mixins import (
    ShowHideViewMixin, SubjectIdentifierViewMixin, VisitScheduleViewMixin, MetaDataViewMixin)

from household.views.mixins import HouseholdViewMixin, HouseholdStructureViewMixin
from member.views import HouseholdMemberViewMixin

from ..appointment_view_mixin import AppointmentViewMixin
from ..consent_view_mixin import ConsentViewMixin

from .subject_locator_view_mixin import SubjectLocatorViewMixin


class DashboardViewMixin(
        SubjectLocatorViewMixin, ShowHideViewMixin, SubjectIdentifierViewMixin,
        HouseholdViewMixin, HouseholdStructureViewMixin, HouseholdMemberViewMixin,
        ConsentViewMixin, VisitScheduleViewMixin,
        AppointmentViewMixin, MetaDataViewMixin):
    pass
