from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_base.fieldsets.fieldset import Fieldset

from bcpp_visit_schedule.constants import T0, E0

from ..admin_site import bcpp_subject_admin
from ..forms import DemographicsForm
from ..models import Demographics
from .modeladmin_mixins import CrfModelAdminMixin


religion_and_ethnicity_fieldset = Fieldset(
    'religion', 'religion_other', 'ethnic', 'ethnic_other',
    section='Religion and Ethnicity')


@admin.register(Demographics, site=bcpp_subject_admin)
class DemographicsAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = DemographicsForm

    conditional_fieldsets = {
        T0: religion_and_ethnicity_fieldset,
        E0: religion_and_ethnicity_fieldset}

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'marital_status',
                'num_wives',
                'husband_wives',
                'live_with')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'marital_status': admin.VERTICAL,
        'religion': admin.VERTICAL,
        'ethnic': admin.VERTICAL,
    }

    filter_horizontal = ('live_with', )
