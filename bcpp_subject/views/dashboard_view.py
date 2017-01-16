from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import MALE
from edc_dashboard.view_mixins import SubjectDashboardViewMixin, DashboardViewMixin
from edc_dashboard.url_mixins.next_url_mixin import NextUrlMixin

from household.views import HouseholdViewMixin, HouseholdStructureViewMixin
from member.views import HouseholdMemberViewMixin
from survey.view_mixins import SurveyViewMixin

from ..models import SubjectConsent, SubjectVisit, SubjectOffstudy, SubjectLocator

from .mixins import SubjectAppConfigViewMixin
from .wrappers import DashboardSubjectConsentModelWrapper, AppointmentModelWrapper


class BcppDashboardNextUrlMixin(NextUrlMixin):

    @property
    def next_url_parameters(self):
        """Add these additional parameters to the next url."""
        parameters = super().next_url_parameters
        parameters['appointment'].append('survey')
        parameters['crfs'].append('survey')
        parameters['visit'].extend(['household_member', 'survey'])
        return parameters

    def appointment_wrapper(self, obj, **options):
        """Add survey object to appointment(s)."""
        obj = super().appointment_wrapper(obj, **options)
        return obj


class DashboardView(
        EdcBaseViewMixin, DashboardViewMixin, SubjectDashboardViewMixin, SurveyViewMixin,
        SubjectAppConfigViewMixin,
        HouseholdViewMixin, HouseholdStructureViewMixin, HouseholdMemberViewMixin,
        BcppDashboardNextUrlMixin, TemplateView):

    add_visit_url_name = SubjectVisit().admin_url_name
    # template_name = 'bcpp_subject/dashboard.html'
    visit_model = SubjectVisit
    consent_model = SubjectConsent

    consent_model_wrapper_class = DashboardSubjectConsentModelWrapper
    appointment_model_wrapper_class = AppointmentModelWrapper

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
        try:
            subject_locator = SubjectLocator.objects.get(
                subject_identifier=self.subject_identifier)
        except SubjectLocator.DoesNotExist:
            subject_locator = None
        context.update(
            navbar_selected='bcpp_subject',
            MALE=MALE,
            visit_url=SubjectVisit().get_absolute_url(),
            subject_offstudy=subject_offstudy,
            subject_locator=subject_locator,
            # enrollment_objects=self.enrollment_objects,
            reference_datetime=get_utcnow(),
        )
        return context

    @property
    def enrollment_objects(self):
        """ """
        # TODO: what are these for? HIC Enrollment?? consents?? what?
        enrollment_objects = []
        enrollments_models = []
        for model in enrollments_models:
            model = django_apps.get_model(*model.split('.'))
            try:
                enrollment_objects.append(
                    model.objects.get(subject_identifier=self.subject_identifier))
            except model.DoesNotExist:
                enrollment_objects.append(model())
            except MultipleObjectsReturned:
                for obj in model.objects.filter(
                        subject_identifier=self.subject_identifier).order_by('version'):
                    enrollment_objects.append(obj)
        return enrollment_objects
