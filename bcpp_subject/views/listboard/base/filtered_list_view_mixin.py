from edc_dashboard.view_mixins import FilteredListViewMixin as BaseFilteredListViewMixin

from ....models import SubjectConsent

from ...dashboard.default.wrappers import SubjectConsentModelWrapper


class FilteredListViewMixin(BaseFilteredListViewMixin):

    filter_model = SubjectConsent
    filtered_model_wrapper_class = SubjectConsentModelWrapper
    filtered_queryset_ordering = '-modified'
    url_lookup_parameters = [
        ('id', 'id'),
        ('subject_identifier', 'subject_identifier'),
    ]
