from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..models import HivTestingHistory
from ..forms import HivTestingHistoryForm

from .modeladmin_mixins import CrfModelAdminMixin
from django.utils.safestring import mark_safe


@admin.register(HivTestingHistory, site=bcpp_subject_admin)
class HivTestingHistoryAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HivTestingHistoryForm

    custom_form_labels = {
        'has_tested': {
            'label': (
                'Since we last saw you in {previous}, '
                'have you tested for HIV?'),
            'callback': lambda obj: True}
    }

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'has_tested',
                'when_hiv_test',
                'has_record',
                'verbal_hiv_result',
                'other_record')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'has_tested': admin.VERTICAL,
        'when_hiv_test': admin.VERTICAL,
        'has_record': admin.VERTICAL,
        'verbal_hiv_result': admin.VERTICAL,
        'other_record': admin.VERTICAL}

    additional_instructions = mark_safe(
        'Do not include documentation of ART/PMTCT/CD4 here; '
        'only include actual HIV test results'
        '<H5><span style=\"color:orange;\">Read to Participant</span></H5>'
        'Many people have had a test'
        ' to see if they have HIV. I am going to ask you'
        ' about whether you have been tested for HIV and'
        ' whether you received the results. Please'
        ' remember that all of your answers are'
        ' confidential.')
