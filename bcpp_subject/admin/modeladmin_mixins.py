from django.contrib import admin
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch

from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin, audit_fieldset_tuple)
from edc_base.fieldsets import FieldsetsModelAdminMixin
from edc_visit_tracking.modeladmin_mixins import (
    CrfModelAdminMixin as VisitTrackingCrfModelAdminMixin)
from edc_base.fieldsets.fieldlist import Remove

from ..constants import T0, T1, T2, T3, E0


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin, admin.ModelAdmin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'


class CrfModelAdminMixin(VisitTrackingCrfModelAdminMixin,
                         FieldsetsModelAdminMixin, ModelAdminMixin):

    instructions = (
        'Please complete the questions below. Required questions are in bold. '
        'When all required questions are complete click SAVE. '
        'Based on your responses, additional questions may be '
        'required or some answers may need to be corrected.')

    def view_on_site(self, obj):
        household_member = obj.subject_visit.household_member
        try:
            return reverse(
                'bcpp-subject:dashboard_url', kwargs=dict(
                    subject_identifier=household_member.subject_identifier,
                    household_identifier=(household_member.household_structure.
                                          household.household_identifier),
                    survey=obj.subject_visit.survey_object.field_value,
                    survey_schedule=obj.subject_visit.survey_schedule_object.field_value))
        except NoReverseMatch:
            return super().view_on_site(obj)


class SexualPartnerAdminMixin:

    conditional_fieldlist = {
        T0: Remove(['first_exchange_age', 'first_exchange_age_other']),
        T1: Remove(['first_exchange']),
        T2: Remove(['first_exchange']),
        T3: Remove(['first_exchange']),
        E0: Remove(['first_exchange']),
    }

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'first_partner_live',
                'sex_partner_community',
                'third_last_sex',
                'third_last_sex_calc',
                'first_first_sex',
                'first_first_sex_calc',
                'first_sex_current',
                'first_relationship',
                'first_relationship_other',
                'first_exchange',
                'first_exchange_age',
                'first_exchange_age_other',
                'concurrent',
                'goods_exchange',
                'first_sex_freq',
                'first_partner_hiv',
                'partner_hiv_test',
                'first_haart',
                'first_disclose',
                'first_condom_freq',
                'first_partner_cp')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'third_last_sex': admin.VERTICAL,
        'first_first_sex': admin.VERTICAL,
        'first_sex_current': admin.VERTICAL,
        'first_relationship': admin.VERTICAL,
        'concurrent': admin.VERTICAL,
        'sex_partner_community': admin.VERTICAL,
        'past_year_sex_freq': admin.VERTICAL,
        'goods_exchange': admin.VERTICAL,
        'first_exchange': admin.VERTICAL,
        'first_exchange_age': admin.VERTICAL,
        'first_partner_hiv': admin.VERTICAL,
        'partner_hiv_test': admin.VERTICAL,
        'first_haart': admin.VERTICAL,
        'first_disclose': admin.VERTICAL,
        'first_condom_freq': admin.VERTICAL,
        'first_partner_cp': admin.VERTICAL, }

    filter_horizontal = ('first_partner_live',)
