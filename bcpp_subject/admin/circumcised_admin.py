from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import CircumcisedForm
from ..models import Circumcised
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Circumcised, site=bcpp_subject_admin)
class CircumcisedAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CircumcisedForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_visit',
                'circumcised',
                'health_benefits_smc',
                'circ_date',
                'when_circ',
                'age_unit_circ',
                'where_circ',
                'where_circ_other',
                'why_circ',
                'why_circ_other'
            ]}), audit_fieldset_tuple)

    radio_fields = {
        'circumcised': admin.VERTICAL,
        'where_circ': admin.VERTICAL,
        'age_unit_circ': admin.VERTICAL,
        'why_circ': admin.VERTICAL, }

    filter_horizontal = ('health_benefits_smc',)
