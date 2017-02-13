from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_constants.constants import NO

from ..admin_site import bcpp_subject_admin
from ..constants import ANNUAL
from ..forms import CircumcisionForm, CircumcisedForm, UncircumcisedForm
from ..models import Circumcision, Circumcised, Uncircumcised
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Circumcision, site=bcpp_subject_admin)
class CircumcisionAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CircumcisionForm

    custom_form_labels = {
        'circumcised': {
            'label': 'Since we last saw you in {previous}, were you circumcised?',
            'callback': lambda obj: True if obj.circumcised == NO else False}
    }

    fieldsets = (
        (None, {
            'fields': [
                'subject_visit',
                'circumcised',
                'circumcised_location',
                'circumcised_location_other',
            ]}), audit_fieldset_tuple)

    radio_fields = {
        'circumcised': admin.VERTICAL,
        'circumcised_location': admin.VERTICAL}

    additional_instructions = mark_safe(
        '<H5><span style="color:orange;">Read to Participant</span></H5>'
        'Some men are circumcised. Male circumcision is '
        '[enter site specific word] when the foreskin of the man\'s penis '
        'has been cut off. I would like to ask you a few questions regarding '
        'male circumcision.')


@admin.register(Circumcised, site=bcpp_subject_admin)
class CircumcisedAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CircumcisedForm

    fields = [
        'subject_visit',
        'circumcised',
        'health_benefits_smc',
        'circ_date',
        'when_circ',
        'age_unit_circ',
        'where_circ',
        'where_circ_other',
        'why_circ',
        'why_circ_other']
    custom_exclude = {
        ANNUAL:
            ['when_circ',
             'age_unit_circ']
    }

    radio_fields = {
        'circumcised': admin.VERTICAL,
        'where_circ': admin.VERTICAL,
        'age_unit_circ': admin.VERTICAL,
        'why_circ': admin.VERTICAL, }

    filter_horizontal = ('health_benefits_smc',)


@admin.register(Uncircumcised, site=bcpp_subject_admin)
class UncircumcisedAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = UncircumcisedForm

    fields = (
        'subject_visit',
        'circumcised',
        'health_benefits_smc',
        'reason_circ',
        'reason_circ_other',
        'future_circ',
        'future_reasons_smc',
        'service_facilities',
        'aware_free',)
    radio_fields = {
        'circumcised': admin.VERTICAL,
        'reason_circ': admin.VERTICAL,
        'future_circ': admin.VERTICAL,
        'future_reasons_smc': admin.VERTICAL,
        'service_facilities': admin.VERTICAL,
        'aware_free': admin.VERTICAL}
    filter_horizontal = ('health_benefits_smc',)
