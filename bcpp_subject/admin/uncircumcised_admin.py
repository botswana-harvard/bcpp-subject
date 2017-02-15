from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_base.fieldsets import Remove

from ..admin_site import bcpp_subject_admin
from ..constants import T1, T2, T3
from ..forms import UncircumcisedForm
from ..models import Uncircumcised
from .modeladmin_mixins import CrfModelAdminMixin

fields = ('circumcised', 'health_benefits_smc',
          'future_circ', 'future_reasons_smc')


@admin.register(Uncircumcised, site=bcpp_subject_admin)
class UncircumcisedAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = UncircumcisedForm

    conditional_fieldlists = {
        T1: Remove(*fields),
        T2: Remove(*fields),
        T3: Remove(*fields),
    }

    fieldsets = (
        (None, {
            'fields': [
                'subject_visit',
                'circumcised',
                'health_benefits_smc',
                'reason_circ',
                'reason_circ_other',
                'future_circ',
                'future_reasons_smc',
                'service_facilities',
                'aware_free',
            ]}), audit_fieldset_tuple)

    radio_fields = {
        'circumcised': admin.VERTICAL,
        'reason_circ': admin.VERTICAL,
        'future_circ': admin.VERTICAL,
        'future_reasons_smc': admin.VERTICAL,
        'service_facilities': admin.VERTICAL,
        'aware_free': admin.VERTICAL}
    filter_horizontal = ('health_benefits_smc',)
