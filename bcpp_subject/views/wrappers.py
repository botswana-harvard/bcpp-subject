from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from django.urls.base import reverse

from edc_appointment.views import AppointmentModelWrapper
from edc_model_wrapper import ModelWrapper


class ModelWrapperMixin(ModelWrapper):

    next_url_name = django_apps.get_app_config(
        'bcpp_subject').dashboard_url_name
    extra_querystring_attrs = {}
    next_url_attrs = {'bcpp_subject.appointment': [
        'household_identifier', 'subject_identifier', 'survey_schedule', 'survey']}
    url_instance_attrs = [
        'household_identifier', 'subject_identifier', 'survey_schedule', 'survey']

    def add_extra_attributes_after(self):
        super().add_extra_attributes_after()
        self.survey = self._original_object.survey
        self.survey_schedule = self._original_object.survey_schedule

    @property
    def survey_object(self):
        return self._original_object.survey_object

    @property
    def survey_schedule_object(self):
        return self._original_object.survey_schedule_object

    @property
    def members(self):
        return (self._original_object
                .household_member
                .household_structure
                .householdmember_set.all())

    @property
    def plot_identifier(self):
        return (self._original_object
                .household_member
                .household_structure
                .household
                .plot
                .plot_identifier)

    @property
    def household_identifier(self):
        return (self._original_object
                .household_member
                .household_structure
                .household
                .household_identifier)

    @property
    def community_name(self):
        return self._original_object.survey_schedule_object.map_area_display


class SubjectVisitModelWrapper(ModelWrapperMixin):

    model_name = 'bcpp_subject.subjectvisit'
    extra_querystring_attrs = {
        'bcpp_subject.subjectvisit': ['household_member']}
    next_url_attrs = {'bcpp_subject.subjectvisit': [
        'appointment', 'household_identifier', 'subject_identifier',
        'survey_schedule', 'survey']}
    url_instance_attrs = [
        'household_identifier', 'subject_identifier', 'survey_schedule', 'survey',
        'appointment', 'household_member']


class AppointmentModelWrapper(AppointmentModelWrapper, ModelWrapperMixin):

    model_name = 'bcpp_subject.appointment'
    visit_model_wrapper_class = SubjectVisitModelWrapper
    dashboard_url_name = django_apps.get_app_config(
        'bcpp_subject').dashboard_url_name

    @property
    def visit(self):
        """Returns a wrapped persistent or non-persistent visit
        instance.
        """
        # FIXME: to much overriden from super class
        # only difference are the options for the visit model
        try:
            return self.visit_model_wrapper_class(self._original_object.subjectvisit)
        except ObjectDoesNotExist:
            visit_model = django_apps.get_model(
                *self.visit_model_wrapper_class.model_name.split('.'))
            return self.visit_model_wrapper_class(
                visit_model(
                    household_member=self._original_object.household_member,
                    appointment=self._original_object,
                    subject_identifier=self.subject_identifier,
                    survey_schedule=self.survey_schedule_object.field_value,
                    survey=self.survey_object.field_value))

    @property
    def forms_url(self):
        """Returns a reversed URL to show forms for this
        appointment/visit.

        This is standard for edc_dashboard
        """
        # FIXME: to much overriden from super class
        # only difference are the extra kwargs tp reverse
        kwargs = dict(
            subject_identifier=self.subject_identifier,
            appointment=self._original_object.id,
            household_identifier=self.household_identifier,
            survey=self.survey_object.field_value,
            survey_schedule=self.survey_schedule_object.field_value)
        return reverse(self.dashboard_url_name, kwargs=kwargs)


class CrfModelWrapper(ModelWrapper):

    admin_site_name = django_apps.get_app_config(
        'bcpp_subject').admin_site_name
    url_namespace = 'bcpp_subject'
    next_url_name = django_apps.get_app_config(
        'bcpp_subject').dashboard_url_name
    next_url_attrs = dict(crf=[
        'appointment', 'household_identifier', 'subject_identifier',
        'survey_schedule', 'survey'])
    extra_querystring_attrs = {
        'crf': ['subject_visit']}
    url_instance_attrs = [
        'appointment', 'household_identifier', 'subject_identifier',
        'survey_schedule', 'survey', 'subject_visit']

    @property
    def appointment(self):
        return self._original_object.subject_visit.appointment

    @property
    def household_member(self):
        return self._original_object.subject_visit.household_member

    @property
    def survey(self):
        return self._original_object.subject_visit.survey

    @property
    def survey_schedule(self):
        return self._original_object.subject_visit.survey_schedule

    @property
    def survey_object(self):
        return self._original_object.subject_visit.survey_object

    @property
    def survey_schedule_object(self):
        return self._original_object.subject_visit.survey_schedule_object

    @property
    def household_identifier(self):
        return (self._original_object
                .subject_visit
                .household_member
                .household_structure
                .household
                .household_identifier)


class SubjectLocatorModelWrapper(ModelWrapper):
    model_name = 'bcpp_subject.subjectlocator'
    admin_site_name = django_apps.get_app_config(
        'bcpp_subject').admin_site_name
    url_namespace = 'bcpp_subject'
    next_url_name = django_apps.get_app_config(
        'bcpp_subject').dashboard_url_name
    next_url_attrs = {'bcpp_subject.subjectlocator': [
        'subject_identifier', 'household_identifier',
        'survey_schedule']}
    url_instance_attrs = [
        'subject_identifier', 'household_identifier',
        'survey_schedule']


class RequisitionModelWrapper(ModelWrapper):

    admin_site_name = django_apps.get_app_config(
        'bcpp_subject').admin_site_name
    url_namespace = 'bcpp_subject'
    next_url_name = django_apps.get_app_config(
        'bcpp_subject').dashboard_url_name
    next_url_attrs = dict(requisition=[
        'appointment', 'household_identifier', 'subject_identifier',
        'survey_schedule', 'survey'])
    extra_querystring_attrs = {
        'requisition': ['subject_visit', 'panel_name']}
    url_instance_attrs = [
        'appointment', 'household_identifier', 'subject_identifier',
        'survey_schedule', 'survey', 'subject_visit', 'panel_name']

    @property
    def subject_visit(self):
        return self._original_object.subject_visit

    @property
    def appointment(self):
        return self._original_object.subject_visit.appointment

    @property
    def household_member(self):
        return self.subject_visit.household_member

    @property
    def survey(self):
        return self.subject_visit.survey

    @property
    def survey_schedule(self):
        return self.subject_visit.survey_schedule

    @property
    def survey_object(self):
        return self.subject_visit.survey_object

    @property
    def survey_schedule_object(self):
        return self.subject_visit.survey_schedule_object

    @property
    def household_identifier(self):
        return (self.household_member
                .household_structure
                .household
                .household_identifier)


class SubjectConsentModelWrapper(ModelWrapper):

    model_name = 'bcpp_subject.subjectconsent'
    next_url_name = django_apps.get_app_config(
        'bcpp_subject').dashboard_url_name
    next_url_attrs = {'bcpp_subject.subjectconsent': [
        'household_identifier', 'subject_identifier', 'survey_schedule']}
    extra_querystring_attrs = {
        'bcpp_subject.subjectconsent': [
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
    def plot_identifier(self):
        return (self._original_object.household_member.
                household_structure.household.plot.plot_identifier)

    @property
    def first_name(self):
        return self._original_object.household_member.first_name

    @property
    def gender(self):
        return self._original_object.household_member.gender

    @property
    def members(self):
        return (self._original_object.household_member.
                household_structure.householdmember_set.all().
                order_by('first_name'))


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
