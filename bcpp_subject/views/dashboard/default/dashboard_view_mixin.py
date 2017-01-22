from edc_dashboard.view_mixins import (
    ShowHideViewMixin, SubjectIdentifierViewMixin, VisitScheduleViewMixin, MetaDataViewMixin)

from household.views.mixins import HouseholdViewMixin, HouseholdStructureViewMixin
from member.views import HouseholdMemberViewMixin

from ....models import SubjectOffstudy

from ..appointment_view_mixin import AppointmentViewMixin
from ..consent_view_mixin import ConsentViewMixin
from ..enrollment_forms_view_mixin import EnrollmentFormsViewMixin

from .subject_locator_view_mixin import SubjectLocatorViewMixin


class DashboardViewMixin(
        EnrollmentFormsViewMixin, SubjectLocatorViewMixin,
        HouseholdViewMixin, HouseholdStructureViewMixin, HouseholdMemberViewMixin,
        ConsentViewMixin, VisitScheduleViewMixin,
        AppointmentViewMixin, MetaDataViewMixin,
        ShowHideViewMixin, SubjectIdentifierViewMixin):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            subject_offstudy = SubjectOffstudy.objects.get(
                subject_identifier=self.subject_identifier)
        except SubjectOffstudy.DoesNotExist:
            subject_offstudy = None
        context.update(
            subject_offstudy=subject_offstudy,
        )
        return context
