from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..models import SubjectRequisition
from ..forms import SubjectRequisitionForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SubjectRequisition, site=bcpp_subject_admin)
class SubjectRequisitionAdmin (CrfModelAdminMixin, admin.ModelAdmin):

    fields = [
            'subject_visit',
            'panel_name',
            'requisition_identifier',
            'drawn_datetime',
            'is_drawn',
            'reason_not_drawn',
            'specimen_identifier',
            'study_site',
            'specimen_type',
            'item_type',
            'item_count',
            'estimated_volume',
            'comments',
        ]
    form = SubjectRequisitionForm

    radio_fields = {
            'is_drawn': admin.VERTICAL,
            'item_type': admin.VERTICAL,
        }