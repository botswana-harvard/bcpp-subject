from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import AccessToCareForm
from ..models import AccessToCare
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(AccessToCare, site=bcpp_subject_admin)
class AccessToCareAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = AccessToCareForm

    additional_instructions = mark_safe(
        '<H5><span style="color:orange;">Read to Participant</span></H5>'
        'Now, I will be asking you '
        'about your preferences and options for accessing '
        'health care when you need it.')

    fieldsets = (
        (None, {
            'fields': [
                'subject_visit',
                'report_datetime',
                'access_care',
                'access_care_other',
                'medical_care_access',
                'medical_care_access_other',
                'overall_access',
                'emergency_access',
                'expensive_access',
                'convenient_access',
                'whenever_access',
                'local_hiv_care',
            ]}), audit_fieldset_tuple)

    radio_fields = {
        'access_care': admin.VERTICAL,
        'overall_access': admin.VERTICAL,
        'emergency_access': admin.VERTICAL,
        'expensive_access': admin.VERTICAL,
        'convenient_access': admin.VERTICAL,
        'whenever_access': admin.VERTICAL,
        'local_hiv_care': admin.VERTICAL}

    filter_horizontal = (
        'medical_care_access',)
