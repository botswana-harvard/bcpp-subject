from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ....models import AnonymousConsent

from ...dashboard.anonymous.wrappers import AnonymousConsentModelWrapper

from ..base import ListboardView as BaseListboardView, FilteredListViewMixin, SearchViewMixin


class ListboardView(FilteredListViewMixin, SearchViewMixin, BaseListboardView):

    navbar_item_selected = 'bcpp_subject'
    navbar_name = 'anonymous'
    filter_model = AnonymousConsent
    filtered_model_wrapper_class = AnonymousConsentModelWrapper

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @property
    def filtered_queryset(self):
        qs = super().filtered_queryset
        plot_identifier = django_apps.get_app_config('plot').anonymous_plot_identifier
        return qs.filter(
            household_member__household_structure__household__plot__plot_identifier=plot_identifier).order_by(
                self.filtered_queryset_ordering)

    def search_queryset(self, search_term, **kwargs):
        qs = super().search_queryset(search_term, **kwargs)
        plot_identifier = django_apps.get_app_config('plot').anonymous_plot_identifier
        return qs.filter(
            household_member__household_structure__household__plot__plot_identifier=plot_identifier).order_by(
                self.filtered_queryset_ordering)
