from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..models import Cd4History
from ..forms import Cd4HistoryForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Cd4History, site=bcpp_subject_admin)
class Cd4HistoryAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = Cd4HistoryForm
    fieldsets = (
        (None, {
            'fields': [
                'subject_visit',
                'record_available',
                'last_cd4_count',
                'last_cd4_drawn_date',
            ]}), audit_fieldset_tuple)

    radio_fields = {
        'record_available': admin.VERTICAL}
