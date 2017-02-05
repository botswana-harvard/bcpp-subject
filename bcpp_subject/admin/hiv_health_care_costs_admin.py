from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import HivHealthCareCostsForm
from ..models import HivHealthCareCosts

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivHealthCareCosts, site=bcpp_subject_admin)
class HivHealthCareCostsAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HivHealthCareCostsForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_visit',
                'hiv_medical_care',
                'reason_no_care',
                'place_care_received',
                'care_regularity',
                'doctor_visits',
            ]}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'hiv_medical_care': admin.VERTICAL,
        'reason_no_care': admin.VERTICAL,
        'place_care_received': admin.VERTICAL,
        'care_regularity': admin.VERTICAL,
        'doctor_visits': admin.VERTICAL,
    }
