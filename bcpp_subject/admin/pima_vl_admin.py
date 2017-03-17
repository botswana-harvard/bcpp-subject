from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..models import PimaVl
from ..forms import PimaVlForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(PimaVl, site=bcpp_subject_admin)
class PimaVlAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = PimaVlForm

    fieldsets = (
        (None, {
            'fields': (
                "subject_visit",
                'test_done',
                'reason_not_done',
                'reason_not_done_other',
                'machine_identifier',
                'test_datetime',
                'result_datetime',
                'result_value',
                'quantifier',
                'easy_of_use',
                'stability')}),
        audit_fieldset_tuple,
    )

    list_filter = ('subject_visit', 'test_datetime', 'machine_identifier')

    list_display = (
        'subject_visit', 'test_datetime', 'result_value', 'machine_identifier')

    radio_fields = {
        'test_done': admin.VERTICAL,
        'reason_not_done': admin.VERTICAL,
        'quantifier': admin.VERTICAL,
        'easy_of_use': admin.VERTICAL}
