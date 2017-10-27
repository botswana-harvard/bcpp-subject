from django.contrib import admin
from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import CeaOpdForm
from ..models import CeaOpd
from .modeladmin_mixins import ModelAdminMixin


@admin.register(CeaOpd, site=bcpp_subject_admin)
class CeaOpdAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CeaOpdForm
    fieldsets = (
        (None, {
            'fields': [
                'subject_visit',
                'care_sought',
                'times_care_sought',
                'times_care_obtained',
                'lab_tests_ordered',
                'tests_ordered',
                'ordered_other',
                'procedures_performed',
                'procedure',
                'medication',
                'medication_prescribed',
                'prescribed_other',
                'further_evaluation',
                'evaluation_referred',
                'cd4_date',
                'cd4_result',
            ]}), audit_fieldset_tuple)

    radio_fields = {
        'care_sought': admin.VERTICAL,
        'lab_tests_ordered': admin.VERTICAL,
        'procedures_performed': admin.VERTICAL,
        'tests_ordered': admin.VERTICAL,
        'medication': admin.VERTICAL,
        'medication_prescribed': admin.VERTICAL,
        'further_evaluation': admin.VERTICAL}
