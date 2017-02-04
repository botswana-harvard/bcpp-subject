from edc_dashboard.view_mixins import (
    ShowHideViewMixin, SubjectIdentifierViewMixin,
    MetaDataViewMixin)

from household.views.mixins import (
    HouseholdViewMixin, HouseholdStructureViewMixin,
    HouseholdLogEntryViewMixin)
from member.views import HouseholdMemberViewMixin

from ..appointment_view_mixin import AppointmentViewMixin
from ..consent_view_mixin import ConsentViewMixin
from ..referral_view_mixin import ReferralViewMixin
from ..subject_helper_view_mixin import SubjectHelperViewMixin
from ..visit_schedule_view_mixin import VisitScheduleViewMixin
from .subject_locator_view_mixin import SubjectLocatorViewMixin


class DashboardViewMixin(
        SubjectIdentifierViewMixin, AppointmentViewMixin,
        MetaDataViewMixin, VisitScheduleViewMixin,
        HouseholdViewMixin, HouseholdStructureViewMixin,
        HouseholdLogEntryViewMixin, HouseholdMemberViewMixin,
        ConsentViewMixin, SubjectLocatorViewMixin, SubjectHelperViewMixin,
        ReferralViewMixin,
        ShowHideViewMixin):
    pass
