from django.apps import apps as django_apps

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
