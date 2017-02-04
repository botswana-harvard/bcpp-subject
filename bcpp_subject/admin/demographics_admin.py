from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import DemographicsForm
from ..models import Demographics
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Demographics, site=bcpp_subject_admin)
class DemographicsAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = DemographicsForm

    fieldsets = (
        (None, {
            'fields': (
                "subject_visit",
                'marital_status',
                'num_wives',
                'husband_wives',
                'live_with')}),
        ('Religion and Ethnicity', {
            'fields': (
                'religion',
                'religion_other',
                'ethnic',
                'ethnic_other')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "marital_status": admin.VERTICAL,
        "religion": admin.VERTICAL,
        "ethnic": admin.VERTICAL,
    }

    filter_horizontal = ('live_with', )
