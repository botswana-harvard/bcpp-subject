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
                'pima_today',
                'pima_today_other',
                'pima_today_other_other',
                'pima_id',
                'cd4_value',
                'cd4_datetime')}),
        audit_fieldset_tuple,
    )

    list_filter = (
        'subject_visit', 'cd4_datetime', 'pima_id', Cd4ThreshHoldFilter,)

    list_display = ('subject_visit', 'cd4_datetime', 'cd4_value', 'pima_id')

    radio_fields = {
        'pima_today': admin.VERTICAL,
        'pima_today_other': admin.VERTICAL}
