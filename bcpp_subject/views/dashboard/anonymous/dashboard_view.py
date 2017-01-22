from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import (
    DashboardViewMixin as EdcDashboardViewMixin, AppConfigViewMixin)

from survey.view_mixins import SurveyViewMixin

from ....models import AnonymousConsent
from ...wrappers import (
    CrfModelWrapper, SubjectVisitModelWrapper, RequisitionModelWrapper)
from .dashboard_view_mixin import DashboardViewMixin
from .wrappers import AnonymousConsentModelWrapper, AppointmentModelWrapper


class DashboardView(
        SurveyViewMixin, DashboardViewMixin,
        AppConfigViewMixin, EdcBaseViewMixin,
        EdcDashboardViewMixin, TemplateView):

    app_config_name = 'bcpp_subject'
    navbar_item_selected = 'bcpp_subject'
    navbar_name = 'anonymous'
    consent_model_wrapper_class = AnonymousConsentModelWrapper
    consent_model = AnonymousConsent
    crf_model_wrapper_class = CrfModelWrapper
    requisition_model_wrapper_class = RequisitionModelWrapper
    visit_model_wrapper_class = SubjectVisitModelWrapper
    appointment_model_wrapper_class = AppointmentModelWrapper

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
