from django.contrib import admin

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
    instructions = [(
        'Read to Participant: I would like to now ask you '
        'questions about drinking alcohol and smoking.')]
