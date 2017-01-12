from django.apps import apps as django_apps
from django.contrib import admin
from django.urls.base import reverse
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin

from edc_base.modeladmin_mixins import ModelAdminInstitutionMixin, audit_fieldset_tuple, audit_fields,\
    ModelAdminNextUrlRedirectMixin
from edc_consent.modeladmin_mixins import ModelAdminConsentMixin

from ..admin_site import bcpp_subject_admin
from ..forms import SubjectConsentForm
from ..models import SubjectConsent


@admin.register(SubjectConsent, site=bcpp_subject_admin)
class SubjectConsentAdmin(ModelAdminConsentMixin, ModelAdminRevisionMixin,
                          ModelAdminInstitutionMixin, ModelAdminNextUrlRedirectMixin,
                          admin.ModelAdmin):

    form = SubjectConsentForm

    fieldsets = (
        (None, {
            'fields': [
                'household_member',
                'subject_identifier',
                'first_name',
                'last_name',
                'initials',
                'language',
                'is_literate',
                'witness_name',
                'consent_datetime',
                'study_site',
                'gender',
                'dob',
                'guardian_name',
                'is_dob_estimated',
                'citizen',
                'legal_marriage',
                'marriage_certificate',
                'marriage_certificate_no',
                'identity',
                'identity_type',
                'confirm_identity',
                'is_incarcerated',
                'may_store_samples',
                'comment',
                'consent_reviewed',
                'study_questions',
                'assessment_score',
                'consent_copy']}),
        audit_fieldset_tuple)

    search_fields = (
        'household_member__household_structure__household__plot__plot_identifier',
        'household_member__household_structure__household__household_identifier')

    radio_fields = {
        "assessment_score": admin.VERTICAL,
        "consent_copy": admin.VERTICAL,
        "consent_reviewed": admin.VERTICAL,
        "gender": admin.VERTICAL,
        "identity_type": admin.VERTICAL,
        "is_dob_estimated": admin.VERTICAL,
        "is_incarcerated": admin.VERTICAL,
        "is_literate": admin.VERTICAL,
        "is_minor": admin.VERTICAL,
        "language": admin.VERTICAL,
        "may_store_samples": admin.VERTICAL,
        "study_questions": admin.VERTICAL,
        'citizen': admin.VERTICAL,
        'legal_marriage': admin.VERTICAL,
        'marriage_certificate': admin.VERTICAL,
    }

    def redirect_url(self, request, obj, post_url_continue=None):
        kwargs = request.GET.dict()
        redirect_url = super(ModelAdminNextUrlRedirectMixin, self).redirect_url(
            request, obj, post_url_continue)
        if kwargs.get(self.querystring_name):
            url_name = kwargs.get(self.querystring_name).split(',')[0]
            attrs = kwargs.get(self.querystring_name).split(',')[1:]
            kwargs = {k: kwargs.get(k) for k in attrs if kwargs.get(k)}
            kwargs.update(subject_identifier=obj.subject_identifier)
            redirect_url = reverse(url_name, kwargs=kwargs)
        return redirect_url

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj=obj) + audit_fields

    def view_on_site(self, obj):
        return reverse(
            'bcpp-subject:dashboard_url', kwargs=dict(
                subject_identifier=obj.subject_identifier,
                survey=obj.survey,
                survey_schedule=obj.survey_object.survey_schedule.field_value))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            HouseholdMember = django_apps.get_model('member', 'householdmember')
            kwargs["queryset"] = HouseholdMember.objects.filter(id__exact=request.GET.get('household_member'))
        return super(SubjectConsentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
