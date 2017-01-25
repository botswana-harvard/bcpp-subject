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
                'date_tb',
                'dx_tb',
                'dx_tb_other')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'dx_tb': admin.VERTICAL, }

    instructions = [(
        'Note to Interviewer: This form is to be filled for all participants'
        ' even if they do not have a record (on hand) of the diagnosis.')]
