from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import MALE
from edc_dashboard.view_mixins import DashboardViewMixin, AppConfigViewMixin
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from household.views import HouseholdViewMixin, HouseholdStructureViewMixin
from member.views import HouseholdMemberViewMixin
from survey.view_mixins import SurveyViewMixin

from ..models import SubjectConsent, SubjectOffstudy, SubjectLocator

from .dashboard import SubjectDashboardViewMixin, SubjectLocatorViewMixin
from .wrappers import CrfModelWrapper, SubjectVisitModelWrapper


class DashboardView(
        EdcBaseViewMixin, DashboardViewMixin,
        AppConfigViewMixin, SurveyViewMixin, SubjectDashboardViewMixin,
        HouseholdViewMixin, HouseholdStructureViewMixin, HouseholdMemberViewMixin,
        SubjectLocatorViewMixin, TemplateView):

    app_config_name = 'bcpp_subject'

    consent_model = SubjectConsent

    crf_model_wrapper_class = CrfModelWrapper
    visit_model_wrapper_class = SubjectVisitModelWrapper

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            subject_offstudy = SubjectOffstudy.objects.get(
                subject_identifier=self.subject_identifier)
        except SubjectOffstudy.DoesNotExist:
            subject_offstudy = None
        context.update(
            navbar_selected='bcpp_subject',
            MALE=MALE,
            subject_offstudy=subject_offstudy,
            reference_datetime=get_utcnow(),
            enrollment_forms=self.enrollment_forms,
        )
        return context

    @property
    def enrollment_forms(self):
        """Returns a generator of enrollment instances for this subject."""
        for visit_schedule in site_visit_schedules.get_visit_schedules().values():
            for schedule in visit_schedule.schedules.values():
                obj = schedule.enrollment_instance(subject_identifier=self.subject_identifier)
                if obj:
                    yield obj
                else:
                    continue
