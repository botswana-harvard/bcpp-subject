from django.db.models import Q

from edc_dashboard.view_mixins import FilteredListViewMixin
from edc_search.view_mixins import SearchViewMixin

from ..models import SubjectConsent

from .wrappers import ListBoardSubjectConsentModelWrapper


class BcppSubjectFilteredListViewMixin(FilteredListViewMixin):

    filter_model = SubjectConsent
    filtered_model_wrapper_class = ListBoardSubjectConsentModelWrapper
    filtered_queryset_ordering = '-modified'
    url_lookup_parameters = ['id', 'subject_identifier']


class BcppSubjectSearchViewMixin(SearchViewMixin):

    search_model = SubjectConsent
    search_model_wrapper_class = ListBoardSubjectConsentModelWrapper
    search_queryset_ordering = '-modified'

    def search_options_for_date(self, search_term, **kwargs):
        """Adds report_datetime to search by date."""
        q, options = super().search_options_for_date(search_term, **kwargs)
        q = q | (
            Q(report_datetime__date=search_term.date()) |
            Q(consent_datetime__date=search_term.date()))
        return q, options

    def search_options(self, search_term, **kwargs):
        q, options = super().search_options(search_term, **kwargs)
        q = q | (
            Q(subject_identifier__icontains=search_term) |
            Q(identity__exact=search_term) |
            Q(initials__exact=search_term) |
            Q(first_name__exact=search_term) |
            Q(last_name__exact=search_term) |
            Q(household_member__household_structure__household__household_identifier__icontains=search_term) |
            Q(household_member__household_structure__household__plot__plot_identifier__icontains=search_term))
        return q, options
