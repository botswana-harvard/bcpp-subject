from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_base.fieldsets.fieldlist import Remove
from bcpp_visit_schedule.constants import T1, T2, T3


from ..admin_site import bcpp_subject_admin
from ..models import HivMedicalCare
from ..forms import HivMedicalCareForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivMedicalCare, site=bcpp_subject_admin)
class HivMedicalCareAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HivMedicalCareForm

    conditional_fieldlists = {
        T1: Remove('lowest_cd4'),
        T2: Remove('lowest_cd4'),
        T3: Remove('lowest_cd4')
    }

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'first_hiv_care_pos',
                'last_hiv_care_pos',
                'lowest_cd4')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'lowest_cd4': admin.VERTICAL}
