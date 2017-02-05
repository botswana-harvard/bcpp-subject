from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..models import Cancer
from ..forms import CancerForm

from .modeladmin_mixins import CrfModelAdminMixin
from django.utils.safestring import mark_safe


@admin.register(Cancer, site=bcpp_subject_admin)
class CancerAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CancerForm
    fields = (
        'subject_visit',
        'cancer_date',
        'cancer_dx',
        'cancer_dx_other',)
    radio_fields = {'cancer_dx': admin.VERTICAL, }

    additional_instructions = mark_safe(
        '<H5>Note to interviewer</span></H5>'
        'This form is to be filled for all participants '
        'even if they do not have a record (on hand) of the diagnosis.')
