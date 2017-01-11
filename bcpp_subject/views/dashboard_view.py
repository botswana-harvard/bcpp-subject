from django.apps import apps as django_apps
from django.core.exceptions import MultipleObjectsReturned
from django.views.generic import TemplateView

from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import MALE
from edc_dashboard.view_mixins import DashboardMixin

from member.models import HouseholdMember
from survey.site_surveys import site_surveys

from ..models import SubjectConsent, SubjectVisit, SubjectOffstudy, SubjectLocator


class BcppDashboardNextUrlMixin(DashboardMixin):

    @property
    def next_url_parameters(self):
        """Add these additional parameters to the next url."""
        parameters = super().next_url_parameters
        parameters['appointment'].append('survey')
        parameters['crfs'].append('survey')
        parameters['visit'].extend(['household_member', 'survey'])
        return parameters


class BcppDashboardExtraFieldMixin(BcppDashboardNextUrlMixin):

    """Adds extra fields to the instance and context.

    * survey object, `survey` to the context as an attr to the view instance
      from `survey` URL parameter. URL expects survey.field_name.

    * household_member from `household_member` URL parameter
    ."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.survey = None
        self.household_member = None

    def get(self, request, *args, **kwargs):
        """Add survey and household member to the instance."""
        self.survey = site_surveys.get_survey_from_field_value(kwargs.get('survey'))
        kwargs['survey'] = self.survey
        options = dict(
            subject_identifier=self.subject_identifier or kwargs.get('subject_identifier'),
            household_structure__survey=self.survey.field_value)
        try:
            obj = HouseholdMember.objects.get(**options)
        except HouseholdMember.DoesNotExist:
            self.household_member = None  # HouseholdMember.objects.get(subject_identifier_as_pk=kwargs.get('subject_identifier'))
        else:
            self.household_member = self.household_member_wrapper(obj)
            kwargs['household_member'] = self.household_member
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            survey=self.survey,
            household_member=self.household_member,
            household_identifier=self.household_member.household_structure.household.household_identifier,
        )
        return context

    def household_member_wrapper(self, obj):
        """Add survey object and dob to to household_member(s)."""
        obj.dob = obj.enrollmentchecklist.dob
        obj = self.pk_wrapper(obj)  # TODO: needed?
        obj.survey = obj.household_structure.survey_object
        return obj

    def consent_wrapper(self, obj):
        """Add survey object to consent(s)."""
        obj = super().consent_wrapper(obj)
        obj.survey = obj.household_member.household_structure.survey_object
        return obj

    def appointment_wrapper(self, obj, **options):
        """Add survey object to appointment(s)."""
        options.update(survey=self.survey.field_value)
        obj = super().appointment_wrapper(obj, **options)
        obj.survey = self.survey
        return obj


class DashboardView(
        BcppDashboardExtraFieldMixin,
        EdcBaseViewMixin, TemplateView):

    dashboard_url = 'bcpp-subject:dashboard_url'
    base_html = 'bcpp/base.html'
    add_visit_url_name = SubjectVisit().admin_url_name
    template_name = 'bcpp_subject/dashboard.html'
    visit_model = SubjectVisit
    consent_model = SubjectConsent

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
            enrollment_objects=self.enrollment_objects,
            reference_datetime=get_utcnow(),
        )
        return context

    @property
    def enrollment_objects(self):
        """ """
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
