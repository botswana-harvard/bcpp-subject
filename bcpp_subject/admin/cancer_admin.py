from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..models import Cancer
from ..forms import CancerForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Cancer, site=bcpp_subject_admin)
class CancerAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CancerForm
    fields = (
        'subject_visit',
        'date_cancer',
        'dx_cancer',)
    radio_fields = {'dx_cancer': admin.VERTICAL, }
    instructions = [(
        'Note to Interviewer: This form is to be filled for all participants'
        ' even if they do not have a record (on hand) of the diagnosis.')]
