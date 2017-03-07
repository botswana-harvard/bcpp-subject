from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms.main import SubstanceUseForm
from ..models import SubstanceUse
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SubstanceUse, site=bcpp_subject_admin)
class SubstanceUseAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SubstanceUseForm
    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'alcohol',
                'smoke',
                'drug_use')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'alcohol': admin.VERTICAL,
        'smoke': admin.VERTICAL,
        'drug_use': admin.VERTICAL,
    }

    additional_instructions = mark_safe(
        '<H5><span style=\"color:orange;\">Read to Participant</span></H5>'
        'I would like to now ask you '
        'questions about drinking alcohol and smoking.')
