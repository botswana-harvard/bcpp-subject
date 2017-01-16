from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from edc_appointment.views import AppointmentModelWrapper
from edc_consent.views import ConsentModelWrapper
from edc_dashboard.wrappers.model_wrapper import ModelWrapper


class ModelWrapperMixin(ModelWrapper):

    admin_site_name = django_apps.get_app_config('bcpp_subject').admin_site_name
    url_namespace = django_apps.get_app_config('bcpp_subject').url_namespace
    next_url_name = django_apps.get_app_config('bcpp_subject').dashboard_url_name

    extra_querystring_attrs = {}
    next_url_attrs = {'bcpp_subject.appointment': [
        'household_identifier', 'subject_identifier', 'survey_schedule', 'survey']}
    url_instance_attrs = ['household_identifier', 'subject_identifier', 'survey_schedule', 'survey']

    def add_extra_attributes_after(self):
        super().add_extra_attributes_after()
        self.survey_object = self.wrapped_object.survey_object
        self.survey_schedule_object = self.wrapped_object.survey_schedule_object

    @property
    def members(self):
        return self.household_member.household_structure.householdmember_set.all()

    @property
    def plot_identifier(self):
        return self.household_member.household_structure.household.plot.plot_identifier

    @property
    def household_identifier(self):
        return self.household_member.household_structure.household.household_identifier

    @property
    def community_name(self):
        return self.survey_schedule_object.map_area_display


class AppointmentModelWrapper(AppointmentModelWrapper, ModelWrapperMixin):

    model_name = 'bcpp_subject.appointment'

    @property
    def visit(self):
        try:
            return self._original_object.subjectvisit
        except ObjectDoesNotExist:
            return None


class ListBoardSubjectConsentModelWrapper(ConsentModelWrapper, ModelWrapperMixin):

    model_name = 'bcpp_subject.subjectconsent'
    next_url_name = django_apps.get_app_config('bcpp_subject').listboard_url_name


class DashboardSubjectConsentModelWrapper(ConsentModelWrapper, ModelWrapperMixin):

    next_url_name = django_apps.get_app_config('bcpp_subject').dashboard_url_name
    extra_querystring_attrs = {
        'bcpp_subject.subjectconsent': ['gender', 'household_member', 'first_name', 'initials']}
    url_instance_attrs = [
        'subject_identifier', 'survey_schedule', 'survey', 'gender',
        'household_member', 'first_name', 'initials', 'household_identifier']
