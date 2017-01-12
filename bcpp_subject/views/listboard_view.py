from django.apps import apps as django_apps
from django.db.models import Q

from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import MALE
from edc_dashboard.view_mixins import ListboardMixin, FilteredListViewMixin
from edc_dashboard.wrappers import ModelWrapper
from edc_search.view_mixins import SearchViewMixin

from ..models import SubjectConsent

app_config = django_apps.get_app_config('bcpp_subject')


class SubjectConsentModelWrapper(ModelWrapper):

    admin_site_name = django_apps.get_app_config('bcpp_subject').admin_site_name
    url_namespace = django_apps.get_app_config('bcpp_subject').url_namespace
    next_url_name = django_apps.get_app_config('bcpp_subject').listboard_url_name

    model_name = 'bcpp_subject.subjectconsent'
    extra_querystring_attrs = {}
    next_url_attrs = {'bcpp_subject.subjectconsent': ['subject_identifier', 'survey_schedule', 'survey']}
    url_instance_attrs = ['subject_identifier', 'survey_schedule', 'survey']

    @property
    def household_member(self):
        return self._original_object.household_member

    @property
    def members(self):
        return self._original_object.household_member.household_structure.householdmember_set.all()

    @property
    def plot_identifier(self):
        return self._original_object.household_member.household_structure.household.plot.plot_identifier

    @property
    def household_identifier(self):
        return self._original_object.household_member.household_structure.household.household_identifier

    @property
    def community_name(self):
        return self._original_object.household_member.household_structure.survey_object.map_area_display


class ListBoardView(EdcBaseViewMixin, ListboardMixin, FilteredListViewMixin, SearchViewMixin):

    template_name = app_config.listboard_template_name
    listboard_url_name = app_config.listboard_url_name
    search_model = SubjectConsent

    search_model_wrapper_class = SubjectConsentModelWrapper
    search_queryset_ordering = '-modified'

    filter_model = SubjectConsent
    filtered_model_wrapper_class = SubjectConsentModelWrapper
    filtered_queryset_ordering = '-modified'
    url_lookup_parameters = ['id', 'subject_identifier']

    def search_options_for_date(self, search_term, **kwargs):
        """Adds report_datetime to search by date."""
        q, options = super().search_options_for_date(search_term, **kwargs)
        q = q | (
            Q(report_datetime__date=search_term.date()) |
            Q(consent_datetime__date=search_term.date()))
        return q, options

    def search_options(self, search_term, **kwargs):
        q, options = super().search_options(search_term, **kwargs)
        q = q | (
            Q(subject_identifier__icontains=search_term) |
            Q(identity__exact=search_term) |
            Q(initials__exact=search_term) |
            Q(first_name__exact=search_term) |
            Q(last_name__exact=search_term) |
            Q(household_member__household_structure__household__household_identifier__icontains=search_term) |
            Q(household_member__household_structure__household__plot__plot_identifier__icontains=search_term))
        return q, options

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            navbar_selected='bcpp_subject',
            MALE=MALE,
            reference_datetime=get_utcnow(),
            plot_listboard_url_name=django_apps.get_app_config('plot').listboard_url_name,
            household_listboard_url_name=django_apps.get_app_config('household').listboard_url_name,
            member_listboard_url_name=django_apps.get_app_config('member').listboard_url_name,
            enumeration_listboard_url_name=django_apps.get_app_config('enumeration').listboard_url_name,
            dashboard_url_name=django_apps.get_app_config('bcpp_subject').dashboard_url_name,
        )
        return context
