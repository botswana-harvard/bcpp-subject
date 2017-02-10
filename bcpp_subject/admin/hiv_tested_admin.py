from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_base.fieldsets import Remove

from ..admin_site import bcpp_subject_admin
from ..constants import T1, T2, T3, E0
from ..forms import HivTestedForm
from ..models import HivTested

from .modeladmin_mixins import CrfModelAdminMixin


fields = (['num_hiv_tests', 'hiv_pills', 'arvs_hiv_test', 'why_hiv_test'])


@admin.register(HivTested, site=bcpp_subject_admin)
class HivTestedAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HivTestedForm

    conditional_fieldlists = {
        T1: Remove(fields),
        T2: Remove(fields),
        T3: Remove(fields),
        E0: Remove(fields),
    }

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'num_hiv_tests',
                'where_hiv_test',
                'where_hiv_test_other',
                'why_hiv_test',
                'hiv_pills',
                'arvs_hiv_test'),
        }),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'where_hiv_test': admin.VERTICAL,
        'why_hiv_test': admin.VERTICAL,
        'hiv_pills': admin.VERTICAL,
        'arvs_hiv_test': admin.VERTICAL, }
