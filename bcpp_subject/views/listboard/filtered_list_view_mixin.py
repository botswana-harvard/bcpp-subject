from edc_dashboard.view_mixins import FilteredListViewMixin as BaseFilteredListViewMixin

from ...models import SubjectConsent

from ..wrappers import ListBoardSubjectConsentModelWrapper


class FilteredListViewMixin(BaseFilteredListViewMixin):

    filter_model = SubjectConsent
    filtered_model_wrapper_class = ListBoardSubjectConsentModelWrapper
    filtered_queryset_ordering = '-modified'
    url_lookup_parameters = ['id', 'subject_identifier']
