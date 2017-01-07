from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic import TemplateView

from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_search.forms import SearchForm
from edc_search.view_mixins import SearchViewMixin

from ..models import SubjectConsent

app_config = django_apps.get_app_config('bcpp_subject')


class SearchPlotForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse('bcpp-subject:list_url')


class ListView(EdcBaseViewMixin, TemplateView, SearchViewMixin, FormView):

    form_class = SearchPlotForm
    template_name = app_config.list_template_name
    paginate_by = 10
    list_url = 'bcpp-subject:list_url'
    search_model = SubjectConsent

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def search_options(self, search_term, **kwargs):
        q = (
            Q(subject_identifier__icontains=search_term) |
            Q(identity__exact=search_term) |
            Q(first_name__exact=search_term) |
            Q(last_name__exact=search_term) |
            Q(household_member__household_structure__household__household_identifier__icontains=search_term) |
            Q(household_member__household_structure__household__plot__plot_identifier__icontains=search_term) |
            Q(user_created__iexact=search_term) |
            Q(user_modified__iexact=search_term))
        options = {}
        return q, options

    def queryset_wrapper(self, qs):
        results = []
        for obj in qs:
            obj.household_member.str_pk = str(obj.household_member.pk)
            obj.plot_identifier = obj.household_member.household_structure.household.plot.plot_identifier
            obj.household_identifier = obj.household_member.household_structure.household.household_identifier
            survey = obj.household_member.household_structure.survey
            _, obj.survey_year, obj.survey_name, obj.community_name = survey.split('.')
            obj.community_name = ' '.join(obj.community_name.split('_'))
            results.append(obj)
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            navbar_selected='bcpp_subject',
            reference_datetime=get_utcnow())
        return context
