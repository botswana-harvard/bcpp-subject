from django.apps import apps as django_apps

from edc_dashboard.wrappers import ModelWrapper

from bcpp_subject.views.wrappers import (
    AppointmentModelWrapper as BaseAppointmentModelWrapper, ModelWrapperMixin)


class SubjectVisitModelWrapper(ModelWrapperMixin):

    model_name = 'bcpp_subject.subjectvisit'
    next_url_name = django_apps.get_app_config(
        'bcpp_subject').anonymous_dashboard_url_name
    extra_querystring_attrs = {
        'bcpp_subject.subjectvisit': ['household_member']}
    next_url_attrs = {'bcpp_subject.subjectvisit': [
        'appointment', 'household_identifier', 'subject_identifier',
        'survey_schedule', 'survey']}
    url_instance_attrs = [
        'household_identifier', 'subject_identifier', 'survey_schedule', 'survey',
        'appointment', 'household_member']


class AppointmentModelWrapper(BaseAppointmentModelWrapper):
    dashboard_url_name = django_apps.get_app_config(
        'bcpp_subject').anonymous_dashboard_url_name
    visit_model_wrapper_class = SubjectVisitModelWrapper
    next_url_name = django_apps.get_app_config(
        'bcpp_subject').anonymous_dashboard_url_name
    extra_querystring_attrs = {}
    next_url_attrs = {'bcpp_subject.appointment': [
        'household_identifier', 'subject_identifier', 'survey_schedule', 'survey']}
    url_instance_attrs = [
        'household_identifier', 'subject_identifier', 'survey_schedule', 'survey']


class AnonymousConsentModelWrapper(ModelWrapper):

    model_name = 'bcpp_subject.anonymousconsent'
    next_url_name = django_apps.get_app_config(
        'bcpp_subject').anonymous_dashboard_url_name
    next_url_attrs = {'bcpp_subject.anonymousconsent': [
        'household_identifier', 'subject_identifier', 'survey_schedule']}
    extra_querystring_attrs = {
        'bcpp_subject.anonymousconsent': [
            'gender', 'household_member', 'first_name', 'initials']}
    url_instance_attrs = [
        'subject_identifier', 'survey_schedule', 'gender',
        'household_member', 'first_name', 'initials', 'household_identifier']

    @property
    def household_member(self):
        return str(self._original_object.household_member.id)

    @property
    def household_identifier(self):
        return (self._original_object.household_member.
                household_structure.household.household_identifier)

    @property
    def first_name(self):
        return 'anonymous'

    @property
    def gender(self):
        return self._original_object.household_member.gender
