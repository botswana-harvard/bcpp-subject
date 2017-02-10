from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_base.fieldsets import Remove

from ..admin_site import bcpp_subject_admin
from ..forms import HivUntestedForm
from ..models import HivUntested
from ..constants import E0

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivUntested, site=bcpp_subject_admin)
class HivUntestedAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    conditional_fieldlists = {
        E0: Remove('hiv_pills', 'arvs_hiv_test'),
    }

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'why_no_hiv_test',
                'hiv_pills',
                'arvs_hiv_test',),
        }),
        audit_fieldset_tuple,
    )

    form = HivUntestedForm

    radio_fields = {
        "why_no_hiv_test": admin.VERTICAL,
        "hiv_pills": admin.VERTICAL,
        "arvs_hiv_test": admin.VERTICAL, }
