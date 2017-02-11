from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import (
    DashboardViewMixin as EdcDashboardViewMixin, AppConfigViewMixin)
from survey.view_mixins import SurveyViewMixin

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ....models import SubjectConsent, SubjectOffstudy
from ...wrappers import (
    CrfModelWrapper, SubjectVisitModelWrapper, RequisitionModelWrapper,
    SubjectConsentModelWrapper)
from .dashboard_view_mixin import DashboardViewMixin


class DashboardView(
        SurveyViewMixin, DashboardViewMixin,
        AppConfigViewMixin, EdcBaseViewMixin,
        EdcDashboardViewMixin, TemplateView):

    app_config_name = 'bcpp_subject'
    navbar_item_selected = 'bcpp_subject'
    consent_model_wrapper_class = SubjectConsentModelWrapper
    consent_model = SubjectConsent
    crf_model_wrapper_class = CrfModelWrapper
    requisition_model_wrapper_class = RequisitionModelWrapper
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
            subject_offstudy=subject_offstudy,
        )
        return context
