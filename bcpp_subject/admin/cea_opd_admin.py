from django.contrib import admin
from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import CeaOpdForm
from ..models import CeaOpd
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(CeaOpd, site=bcpp_subject_admin)
class CeaOpdAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CeaOpdForm
    
    filter_horizontal = ('tests_ordered', 'medication_prescribed',)

    fieldsets = (
        (None, {
            'fields': [
                'subject_visit',
                'times_care_sought',
                'times_care_obtained',
                'tb_care',
                'hiv_related',
                'hiv_related_none_tb',
                'pregnancy_related',
                'injury_accident',
                'chronic_disease',
                'cancer_care',
                'other_care',
                'other_care_count',
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
        'lab_tests_ordered': admin.VERTICAL,
        'procedures_performed': admin.VERTICAL,
        'medication': admin.VERTICAL,
        'further_evaluation': admin.VERTICAL}
