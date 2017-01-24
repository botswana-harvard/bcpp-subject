from django.contrib import admin

from edc_base.fieldsets import Fieldset

from ..admin_site import bcpp_subject_admin
from ..forms import DemographicsForm
from ..models import Demographics
from ..constants import T1, T2, T3, E0

from .modeladmin_mixins import CrfModelAdminMixin


religion_fields = ('religion', 'religion_other', 'ethnic', 'ethnic_other')


@admin.register(Demographics, site=bcpp_subject_admin)
class DemographicsAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = DemographicsForm

    conditional_fieldsets = {
        T1: Fieldset(*religion_fields, section='Religion'),
        T2: Fieldset(*religion_fields, section='Religion'),
        T3: Fieldset(*religion_fields, section='Religion'),
        E0: Fieldset(*religion_fields, section='Religion'),
    }

    fieldsets = (
        (None, {
            'fields': (
                "subject_visit",
                'religion',
                'religion_other',
                'ethnic',
                'ethnic_other',
                'marital_status',
                'num_wives',
                'husband_wives',
                'live_with'),
        }),
    )

    radio_fields = {
        "marital_status": admin.VERTICAL, }

    filter_horizontal = ('live_with', 'religion', 'ethnic')
