import re

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic import TemplateView

from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_consent.site_consents import site_consents
from edc_constants.constants import MALE, UUID_PATTERN
from edc_dashboard.view_mixins import DashboardMixin
from edc_search.forms import SearchForm
from edc_search.view_mixins import SearchViewMixin

from member.models import HouseholdMember

from .models import SubjectConsent, SubjectVisit, SubjectOffstudy, SubjectLocator

app_config = django_apps.get_app_config('bcpp_subject')


class SearchPlotForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse('bcpp-subject:list_url')


class BcppSubjectsView(EdcBaseViewMixin, TemplateView, SearchViewMixin, FormView):

    form_class = SearchPlotForm
    template_name = app_config.list_template_name
    paginate_by = 10
    list_url = 'bcpp-subject:list_url'
    search_model = SubjectConsent

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def search_options(self, search_term, **kwargs):
        q = (
            Q(subject_identifier__icontains=search_term) |
            Q(identity__exact=search_term) |
            Q(first_name__exact=search_term) |
            Q(last_name__exact=search_term) |
            Q(household_member__household_structure__household__household_identifier__icontains=search_term) |
            Q(household_member__household_structure__household__plot__plot_identifier__icontains=search_term) |
            Q(user_created__iexact=search_term) |
            Q(user_modified__iexact=search_term))
        options = {}
        return q, options

    def queryset_wrapper(self, qs):
        results = []
        for obj in qs:
            obj.household_member.str_pk = str(obj.household_member.pk)
            obj.plot_identifier = obj.household_member.household_structure.household.plot.plot_identifier
            obj.household_identifier = obj.household_member.household_structure.household.household_identifier
            survey = obj.household_member.household_structure.survey
            _, obj.survey_year, obj.survey_name, obj.community_name = survey.split('.')
            obj.community_name = ' '.join(obj.community_name.split('_'))
            results.append(obj)
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            navbar_selected='bcpp_subject',
            reference_datetime=get_utcnow())
        return context


class DashboardView(DashboardMixin, EdcBaseViewMixin, TemplateView):

    dashboard_url = 'bcpp-subject:dashboard_url'
    base_html = 'bcpp/base.html'
    add_visit_url_name = SubjectVisit().admin_url_name
    template_name = 'bcpp_subject/dashboard.html'
    visit_model = SubjectVisit

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def survey_wrapper(self, obj):
        try:
            survey = obj.household_member.household_structure.survey
        except AttributeError:
            survey = obj.household_structure.survey
        _, obj.survey_year, obj.survey_name, obj.community_name = survey.split('.')
        obj.community_name = ' '.join(obj.community_name.split('_'))
        return obj

    def pk_wrapper(self, obj):
        obj.str_pk = str(obj.id)
        return obj

    def subject_consent_wrapper(self, obj):
        obj = self.survey_wrapper(obj)
        obj.consent_object = site_consents.get_consent(
            report_datetime=obj.consent_datetime,
            consent_model=obj._meta.label_lower,
            version=obj.version)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            household_member = HouseholdMember.objects.get(
                subject_identifier=context.get('subject_identifier'),
                household_structure__survey=context.get('survey'))
        except HouseholdMember.DoesNotExist:
            household_member = HouseholdMember.objects.get(
                pk=context.get('member'))
        household_member = self.pk_wrapper(self.survey_wrapper(household_member))
        current_subject_consent = SubjectConsent.consent.consent_for_period(
            household_member.subject_identifier, report_datetime=get_utcnow())
        if current_subject_consent:
            current_subject_consent = self.subject_consent_wrapper(current_subject_consent)
        else:
            current_subject_consent = site_consents.get_consent(
                report_datetime=get_utcnow())
        subject_consents = SubjectConsent.objects.filter(
            household_member=household_member).order_by('version')
        subject_consents = [
            self.subject_consent_wrapper(obj) for obj in subject_consents
            if obj != current_subject_consent]
        subject_identifier = household_member.subject_identifier
        if re.match(UUID_PATTERN, subject_identifier):
            subject_identifier = None
        try:
            subject_offstudy = SubjectOffstudy.objects.get(
                subject_identifier=household_member.subject_identifier)
        except SubjectOffstudy.DoesNotExist:
            subject_offstudy = None
        try:
            subject_locator = SubjectLocator.objects.get(
                subject_identifier=household_member.subject_identifier)
        except SubjectLocator.DoesNotExist:
            subject_locator = None
        context.update(
            navbar_selected='bcpp_subject',
            MALE=MALE,
            visit_url=SubjectVisit().get_absolute_url(),
            member=household_member,
            subject_identifier=subject_identifier,
            household_identifier=household_member.household_structure.household.household_identifier,
            survey=household_member.household_structure.survey,
            current_subject_consent=current_subject_consent,
            subject_consents=subject_consents,
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
