from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from edc_dashboard.forms import SearchForm as BaseSearchForm

from ...models import AnonymousConsent
from ..wrappers import AnonymousConsentModelWrapper
from .base_listboard import BaseListboardView


class SearchForm(BaseSearchForm):
    action_url_name = django_apps.get_app_config(
        'bcpp_subject').anonymous_listboard_url_name


class AnonymousListboardView(BaseListboardView):

    model = AnonymousConsent
    model_wrapper_class = AnonymousConsentModelWrapper
    search_form_class = SearchForm
    paginate_by = 10
    navbar_name = 'anonymous'
    navbar_item_selected = 'bcpp_subject'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(
            request, *args, **kwargs)
        plot_identifier = django_apps.get_app_config(
            'plot').anonymous_plot_identifier
        options.update(
            {'household_member__household_structure__household__plot__plot_identifier': plot_identifier})
        return options
