from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import DashboardMixin
from edc_search.forms import SearchForm
from edc_search.view_mixins import SearchViewMixin

from .models import SubjectConsent
from bcpp_subject.models.subject_visit import SubjectVisit
from edc_base.utils import get_utcnow
from bcpp_subject.models.subject_offstudy import SubjectOffstudy
from bcpp_subject.models.subject_locator import SubjectLocator
from member.models.household_member.household_member import HouseholdMember
from django.core.exceptions import MultipleObjectsReturned

app_config = django_apps.get_app_config('bcpp_subject')


class SearchPlotForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse('bcpp-subject:list_url')


class BcppSubjectsView(EdcBaseViewMixin, TemplateView, SearchViewMixin, FormView):

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
            results.append(obj)
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(navbar_selected='bcpp_subject')
        return context


class DashboardView(DashboardMixin, EdcBaseViewMixin, TemplateView):

    subject_dashboard_url_name = 'bcpp-subject:dashboard_url'
    add_visit_url_name = SubjectVisit().admin_url_name
    template_name = 'bcpp_subject/dashboard.html'
    visit_model = SubjectVisit

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def subject_consent_wrapper(self, obj):
        survey = obj.household_member.household_structure.survey
        _, obj.survey_year, obj.survey_name, obj.community_name = survey.split('.')
        obj.community_name = ' '.join(obj.community_name.split('_'))
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        household_member = HouseholdMember.objects.get(subject_identifier=context.get('subject_identifier'))
        subject_consents = SubjectConsent.objects.filter(household_member=household_member)
        subject_consent = SubjectConsent.consent.consent_for_period(
            household_member.subject_identifier, report_datetime=get_utcnow())
        try:
            subject_offstudy = SubjectOffstudy.objects.get(
                subject_identifier=household_member.subject_identifier)
        except SubjectOffstudy.DoesNotExist:
            subject_offstudy = None
        try:
            subject_locator = SubjectLocator.objects.get(
                subject_identifier=household_member.subject_identifier)
        except SubjectLocator.DoesNotExist:
            subject_locator = None
        context.update(
            visit_url=SubjectVisit().get_absolute_url(),
            member=household_member,
            subject_consent=self.subject_consent_wrapper(subject_consent),
            subject_consents=subject_consents,
            subject_offstudy=subject_offstudy,
            subject_locator=subject_locator,
            enrollment_objects=self.enrollment_objects,
            reference_datetime=get_utcnow(),
        )
        return context

    @property
    def enrollment_objects(self):
        """ """
        enrollment_objects = []
        enrollments_models = ['bcpp_subject.subjectconsent']
        for model in enrollments_models:
            model = django_apps.get_model(*model.split('.'))
            try:
                enrollment_objects.append(
                    model.objects.get(subject_identifier=self.subject_identifier))
            except model.DoesNotExist:
                enrollment_objects.append(model())
            except MultipleObjectsReturned:
                for obj in model.objects.filter(
                        subject_identifier=self.subject_identifier).order_by('version'):
                    enrollment_objects.append(obj)
        return enrollment_objects
