from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..models import Tuberculosis
from ..forms import TuberculosisForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Tuberculosis, site=bcpp_subject_admin)
class TuberculosisAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = TuberculosisForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'tb_date',
                'tb_dx',
                'tb_dx_other')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'tb_dx': admin.VERTICAL, }

    instructions = [(
        'Note to Interviewer: This form is to be filled for all participants'
        ' even if they do not have a record (on hand) of the diagnosis.')]
