from bcpp_referral.referral_view_mixin import ReferralViewMixin
from edc_dashboard.view_mixins import MetaDataViewMixin
from edc_dashboard.view_mixins import ShowHideViewMixin, SubjectIdentifierViewMixin
from household_dashboard.view_mixins import HouseholdLogEntryViewMixin
from household_dashboard.view_mixins import HouseholdViewMixin, HouseholdStructureViewMixin
from member_dashboard.view_mixins import HouseholdMemberViewMixin
from survey.view_mixins import SurveyViewMixin

from ..appointment_view_mixin import AppointmentViewMixin
from ..consent_view_mixin import ConsentViewMixin
from ..subject_helper_view_mixin import SubjectHelperViewMixin
from ..subject_visit_view_mixin import SubjectVisitViewMixin
from ..visit_schedule_view_mixin import VisitScheduleViewMixin


class BaseDashboardView(
        ReferralViewMixin,
        SubjectHelperViewMixin,
        MetaDataViewMixin,
        ConsentViewMixin,
        SubjectVisitViewMixin,
        AppointmentViewMixin,
        VisitScheduleViewMixin,
        HouseholdMemberViewMixin,
        HouseholdLogEntryViewMixin,
        HouseholdStructureViewMixin,
        HouseholdViewMixin,
        SurveyViewMixin,
        ShowHideViewMixin,
        SubjectIdentifierViewMixin):
    pass
