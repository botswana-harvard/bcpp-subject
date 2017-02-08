import re

from django.db.models import Q

from edc_search.view_mixins import SearchViewMixin as BaseSearchViewMixin

from ....models import SubjectConsent

from ...dashboard.default.wrappers import SubjectConsentModelWrapper
from bcpp_subject.patterns import subject_identifier


class SearchViewMixin(BaseSearchViewMixin):

    search_model = SubjectConsent
    search_model_wrapper_class = SubjectConsentModelWrapper
    search_queryset_ordering = '-modified'

    def search_options_for_date(self, search_term, **kwargs):
        """Adds consent datetime to search by date."""
        q, options = super().search_options_for_date(search_term, **kwargs)
        q = q | Q(consent_datetime__date=search_term.date())
        return q, options

    def search_options(self, search_term, **kwargs):
        q, options = super().search_options(search_term, **kwargs)
        if re.match(subject_identifier, search_term):
            q = q | Q(subject_identifier__icontains=search_term)
        else:
            q = q | (
                Q(subject_identifier__icontains=search_term) |
                Q(identity__exact=search_term) |
                Q(initials__exact=search_term) |
                Q(first_name__exact=search_term) |
                Q(last_name__exact=search_term) |
                Q(**{'household_member__household_structure'
                     '__household__household_identifier__icontains': search_term}) |
                Q(**{'household_member__household_structure'
                     '__household__plot__plot_identifier__icontains':
                     search_term})
            )
        print(q, options)
        return q, options
