from edc_dashboard.view_mixins import (
    ShowHideViewMixin, SubjectIdentifierViewMixin,
    VisitScheduleViewMixin, MetaDataViewMixin)

from household.views.mixins import (
    HouseholdViewMixin, HouseholdStructureViewMixin,
    HouseholdLogEntryViewMixin)
from member.views import HouseholdMemberViewMixin

from ..appointment_view_mixin import AppointmentViewMixin
from ..consent_view_mixin import ConsentViewMixin
from ..enrollment_forms_view_mixin import EnrollmentFormsViewMixin

from .subject_locator_view_mixin import SubjectLocatorViewMixin


class DashboardViewMixin(
        SubjectIdentifierViewMixin, AppointmentViewMixin, MetaDataViewMixin,
        VisitScheduleViewMixin, EnrollmentFormsViewMixin, SubjectLocatorViewMixin,
        HouseholdViewMixin, HouseholdStructureViewMixin, HouseholdLogEntryViewMixin,
        HouseholdMemberViewMixin, ConsentViewMixin, ShowHideViewMixin):
    pass
