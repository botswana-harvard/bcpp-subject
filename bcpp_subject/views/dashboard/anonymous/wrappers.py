from django.apps import apps as django_apps

from edc_dashboard.wrappers import ModelWrapper

from ...wrappers import (
    AppointmentModelWrapper as BaseAppointmentModelWrapper,
    CrfModelWrapper as BaseCrfModelWrapper,
    SubjectVisitModelWrapper as BaseSubjectVisitModelWrapper,
    RequisitionModelWrapper as BaseRequisitionModelWrapper)


class CrfModelWrapper(BaseCrfModelWrapper):

    next_url_name = django_apps.get_app_config(
        'bcpp_subject').anonymous_dashboard_url_name


class RequisitionModelWrapper(BaseRequisitionModelWrapper):

    next_url_name = django_apps.get_app_config(
        'bcpp_subject').anonymous_dashboard_url_name


class SubjectVisitModelWrapper(BaseSubjectVisitModelWrapper):

    next_url_name = django_apps.get_app_config(
        'bcpp_subject').anonymous_dashboard_url_name


class AppointmentModelWrapper(BaseAppointmentModelWrapper):
    dashboard_url_name = django_apps.get_app_config(
        'bcpp_subject').anonymous_dashboard_url_name
    visit_model_wrapper_class = SubjectVisitModelWrapper
    next_url_name = django_apps.get_app_config(
        'bcpp_subject').anonymous_dashboard_url_name


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
        'household_member', 'first_name', 'initials',
        'household_identifier']

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
