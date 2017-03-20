import re
import socket

from django.apps import apps as django_apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator

from edc_map.models import InnerContainer

from ...models import SubjectConsent
from ..wrappers import SubjectConsentModelWrapper
from .base_listboard import BaseListboardView


class ListboardView(BaseListboardView):

    model = SubjectConsent
    model_wrapper_class = SubjectConsentModelWrapper

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset_exclude_options(self, request, *args, **kwargs):
        options = super().get_queryset_exclude_options(
            request, *args, **kwargs)
        plot_identifier = django_apps.get_app_config(
            'plot').anonymous_plot_identifier
        options.update(
            {'household_member__household_structure__household__plot__plot_identifier': plot_identifier})
        return options

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        map_area = settings.CURRENT_MAP_AREA
        options.update(
            {'household_member__household_structure__household__plot__map_area': map_area})
        device_id = socket.gethostname()[-2:]
        plot_identifier_list = []
        try:
            plot_identifier_list = InnerContainer.objects.get(
                device_id=device_id).identifier_labels
        except InnerContainer.DoesNotExist:
            plot_identifier_list = []
        if plot_identifier_list:
            options.update(
                {'household_member__household_structure__household__plot__plot_identifier__in': plot_identifier_list})
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        if kwargs.get('survey_schedule'):
            options.update(
                {'survey_schedule': kwargs.get('survey_schedule')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
