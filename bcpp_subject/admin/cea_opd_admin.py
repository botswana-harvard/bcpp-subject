from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..models import CeaOpd
from ..forms import CeaOpdForm

from .modeladmin_mixins import ModelAdminMixin


@admin.register(CeaOpd, site=bcpp_subject_admin)
class CeaOpdAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CeaOpdForm
    fieldsets = (
        (None, {
            'fields': [
                'care_sought',
                'times_care_sought',
                'times_care_obtained',
                'lab_tests_ordered',
                'tests_ordered',
                'procedures_performed',
                'lab_test',
                'medication',
                'medication_prescribed',
                'further_evaluation',
                'evaluation_referred',
            ]}), audit_fieldset_tuple)

    radio_fields = {
        'care_sought': admin.VERTICAL,
        'lab_tests_ordered': admin.VERTICAL,
        'procedures_performed': admin.VERTICAL,
        'tests_ordered': admin.VERTICAL,
        'medication_prescribed': admin.VERTICAL, }
