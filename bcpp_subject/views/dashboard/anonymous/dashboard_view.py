from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import (
    DashboardViewMixin as EdcDashboardViewMixin, AppConfigViewMixin)

from survey.view_mixins import SurveyViewMixin

from ....models import AnonymousConsent
from .dashboard_view_mixin import DashboardViewMixin
from .wrappers import (
    AnonymousConsentModelWrapper, AppointmentModelWrapper,
    SubjectVisitModelWrapper, CrfModelWrapper, RequisitionModelWrapper)


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

    def get(self, request, *args, **kwargs):
        self.anonymous = True
        kwargs['anonymous'] = 'anonymous'
        kwargs['anonymous_dashboard_url_name'] = django_apps.get_app_config(
            'bcpp_subject').anonymous_dashboard_url_name
        return super().get(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
