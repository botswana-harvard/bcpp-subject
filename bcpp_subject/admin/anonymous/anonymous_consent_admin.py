from django.apps import apps as django_apps
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch

from edc_base.modeladmin_mixins import audit_fieldset_tuple, audit_fields

from survey.admin import survey_fields, survey_fieldset_tuple

from ...admin_site import bcpp_subject_admin
from ...models import AnonymousConsent
from ..modeladmin_mixins import ModelAdminMixin


@admin.register(AnonymousConsent, site=bcpp_subject_admin)
class AnonymousConsentAdmin(ModelAdminMixin, admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': [
                'household_member',
                'subject_identifier',
                'consent_datetime',
                'gender',
                'dob',
                'citizen',
                'may_store_samples']}),
        survey_fieldset_tuple,
        audit_fieldset_tuple)

    list_display = ('subject_identifier', 'consent_datetime', 'version', 'survey',
                    'user_created', 'hostname_created')

    search_fields = (
        'household_member__household_structure__household__plot__plot_identifier',
        'household_member__household_structure__household__household_identifier')

    radio_fields = {
        "gender": admin.VERTICAL,
        "may_store_samples": admin.VERTICAL,
        'citizen': admin.VERTICAL,
    }

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        readonly_fields = readonly_fields + audit_fields + survey_fields
        if obj:
            readonly_fields += (
                'subject_identifier',
                'subject_identifier_as_pk',
                'study_site',
                'consent_datetime',)
        else:
            readonly_fields += ('subject_identifier',
                                'subject_identifier_as_pk',)
        return readonly_fields

    def view_on_site(self, obj):
        try:
            return reverse(
                'bcpp-subject:dashboard_url', kwargs=dict(
                    household_identifier=(
                        obj.household_member.household_structure.household.household_identifier),
                    subject_identifier=obj.subject_identifier,
                    survey=obj.survey,
                    survey_schedule=obj.survey_schedule_object.field_value))
        except NoReverseMatch:
            return super().view_on_site(obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "household_member":
            HouseholdMember = django_apps.get_model(
                'member', 'householdmember')
            kwargs["queryset"] = (
                HouseholdMember.objects.filter(id__exact=request.GET.get('household_member')))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
