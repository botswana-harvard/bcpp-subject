from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_base.fieldsets import Remove
from bcpp_visit_schedule.constants import T1, T2, T3

from ..admin_site import bcpp_subject_admin
from ..forms import LabourMarketWagesForm
from ..models import LabourMarketWages
from .grant_admin import GrantInlineAdmin
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(LabourMarketWages, site=bcpp_subject_admin)
class LabourMarketWagesAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = LabourMarketWagesForm

    inlines = [GrantInlineAdmin, ]

    conditional_fieldlists = {
        T1: Remove('occupation', 'monthly_income'),
        T2: Remove('occupation', 'monthly_income'),
        T3: Remove('occupation', 'monthly_income'),
    }

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'employed',
                'occupation',
                'occupation_other',
                'job_description_change',
                'days_worked',
                'monthly_income',
                'salary_payment',
                'household_income',
                'other_occupation',
                'other_occupation_other',
                'govt_grant',
                'nights_out',
                'weeks_out',
                'days_not_worked',
                'days_inactivite')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'employed': admin.VERTICAL,
        'occupation': admin.VERTICAL,
        'monthly_income': admin.VERTICAL,
        'salary_payment': admin.VERTICAL,
        'household_income': admin.VERTICAL,
        'other_occupation': admin.VERTICAL,
        'govt_grant': admin.VERTICAL,
        'weeks_out': admin.VERTICAL,
    }
