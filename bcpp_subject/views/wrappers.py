from django.apps import apps as django_apps

from edc_dashboard.wrappers import ModelWrapper


class SubjectConsentModelWrapper(ModelWrapper):

    admin_site_name = django_apps.get_app_config('bcpp_subject').admin_site_name
    url_namespace = django_apps.get_app_config('bcpp_subject').url_namespace
    next_url_name = django_apps.get_app_config('bcpp_subject').listboard_url_name

    model_name = 'bcpp_subject.subjectconsent'
    extra_querystring_attrs = {}
    next_url_attrs = {'bcpp_subject.subjectconsent': ['subject_identifier', 'survey_schedule', 'survey']}
    url_instance_attrs = ['subject_identifier', 'survey_schedule', 'survey']

    def add_from_wrapped_model(self):
        super().add_from_wrapped_model()
        self.version = self.wrapped_object.version
        self.verbose_name = self.wrapped_object.verbose_name
        self.consent_datetime = self.wrapped_object.consent_datetime

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
        return self._original_object.survey_schedule_object.map_area_display


class DashboardSubjectConsentModelWrapper(SubjectConsentModelWrapper):
    next_url_name = django_apps.get_app_config('bcpp_subject').dashboard_url_name
    extra_querystring_attrs = {
        'bcpp_subject.subjectconsent': ['gender', 'household_member', 'first_name', 'initials']}
    url_instance_attrs = [
        'subject_identifier', 'survey_schedule', 'survey', 'gender',
        'household_member', 'first_name', 'initials']
