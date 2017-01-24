from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import ImmigrationStatusForm
from ..models import ImmigrationStatus

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(ImmigrationStatus, site=bcpp_subject_admin)
class ImmigrationStatusAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = ImmigrationStatusForm

    fieldsets = (
        (None, {
            'fields': [
                "subject_visit",
                "report_datetime",
                "country_of_origin",
                "immigration_status",
            ]}),
        audit_fieldset_tuple
    )

    radio_fields = {
        "country_of_origin": admin.VERTICAL,
        "immigration_status": admin.VERTICAL}
