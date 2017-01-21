from django.apps import apps as django_apps

from edc_dashboard.wrappers import ModelWrapper


class SubjectConsentModelWrapper(ModelWrapper):

    model_name = 'bcpp_subject.subjectconsent'
    next_url_name = django_apps.get_app_config('bcpp_subject').dashboard_url_name
    next_url_attrs = {'bcpp_subject.subjectconsent': [
        'household_identifier', 'subject_identifier', 'survey_schedule', 'survey']}
    extra_querystring_attrs = {
        'bcpp_subject.subjectconsent': ['gender', 'household_member', 'first_name', 'initials']}
    url_instance_attrs = [
        'subject_identifier', 'survey_schedule', 'survey', 'gender',
        'household_member', 'first_name', 'initials', 'household_identifier']

    @property
    def household_member(self):
        return str(self._original_object.household_member.id)

    @property
    def household_identifier(self):
        return self._original_object.household_member.household_structure.household.household_identifier

    @property
    def plot_identifier(self):
        return self._original_object.household_member.household_structure.household.plot.plot_identifier

    @property
    def first_name(self):
        return self._original_object.household_member.first_name

    @property
    def gender(self):
        return self._original_object.household_member.gender

    @property
    def members(self):
        return self._original_object.household_member.household_structure.householdmember_set.all().order_by('first_name')
