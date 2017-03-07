from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import ElisaHivResultForm
from ..models import ElisaHivResult
from ..filters import HivResultFilter

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(ElisaHivResult, site=bcpp_subject_admin)
class ElisaHivResultAdmin (CrfModelAdminMixin, admin.ModelAdmin):

    form = ElisaHivResultForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'hiv_result',
                'hiv_result_datetime',
            )}),
        audit_fieldset_tuple,
    )

    list_filter = (HivResultFilter,)

    radio_fields = {
        "hiv_result": admin.VERTICAL,
    }
