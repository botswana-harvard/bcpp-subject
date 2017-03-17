from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..filters import Cd4ThreshHoldFilter
from ..forms import PimaCd4Form
from ..models import PimaCd4

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(PimaCd4, site=bcpp_subject_admin)
class PimaCd4Admin(CrfModelAdminMixin, admin.ModelAdmin):

    form = PimaCd4Form

    fieldsets = (
        (None, {
            'fields': (
                "subject_visit",
                'test_done',
                'reason_not_done',
                'reason_not_done_other',
                'machine_identifier',
                'result_datetime'
                'result_value',
            )}),
        audit_fieldset_tuple,
    )

    list_filter = (
        'subject_visit', 'result_datetime', 'machine_identifier', Cd4ThreshHoldFilter,)

    list_display = (
        'subject_visit', 'result_datetime', 'result_value', 'machine_identifier')

    radio_fields = {
        'test_done': admin.VERTICAL,
        'reason_not_done': admin.VERTICAL}
