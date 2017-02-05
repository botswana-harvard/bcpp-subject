from django.contrib import admin
from django.utils.safestring import mark_safe

from ..admin_site import bcpp_subject_admin
from ..forms import HospitalAdmissionForm
from ..models import HospitalAdmission
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HospitalAdmission, site=bcpp_subject_admin)
class HospitalAdmissionAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HospitalAdmissionForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'admission_nights',
                'reason_hospitalized',
                'facility_hospitalized',
                'nights_hospitalized',
                'healthcare_expense',
                'travel_hours',
                'total_expenses',
                'hospitalization_costs')}),
    )

    radio_fields = {
        'reason_hospitalized': admin.VERTICAL,
        'travel_hours': admin.VERTICAL,
        'hospitalization_costs': admin.VERTICAL,
    }

    additional_instructions = mark_safe(
        '<H5><span style="color:orange;">Read to Participant</span></H5>'
        'For the next set of questions please think about times you '
        'were admitted to a hospital in the last 3 months')
