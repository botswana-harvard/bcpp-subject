from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..models import ArvHistory
from ..forms import ArvHistoryForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(ArvHistory, site=bcpp_subject_admin)
class ArvHistoryAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = ArvHistoryForm
    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'arv',
                'date_started',
                'date_stopped')}),
    )

    radio_fields = {'arv': admin.VERTICAL, }

    instructions = [(
        'Note to Interviewer: This form is to be filled for all participants'
        ' even if they do not have a record (on hand) of the diagnosis.')]
