from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..models import HivMedicalCare
from ..forms import HivMedicalCareForm

from .modeladmin_mixins import CrfModelAdminMixin
from edc_base.modeladmin_mixins import audit_fieldset_tuple


@admin.register(HivMedicalCare, site=bcpp_subject_admin)
class HivMedicalCareAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HivMedicalCareForm

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
