from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_lab.admin import (
    RequisitionAdminMixin,
    requisition_fieldset,
    requisition_status_fieldset,
    requisition_identifier_fieldset,
    requisition_identifier_fields)

from ..admin_site import bcpp_subject_admin
from ..models import SubjectRequisition
from ..forms import SubjectRequisitionForm
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SubjectRequisition, site=bcpp_subject_admin)
class SubjectRequisitionAdmin(CrfModelAdminMixin,
                              RequisitionAdminMixin,
                              admin.ModelAdmin):

    form = SubjectRequisitionForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'requisition_datetime',
                'panel_name',
            )}),
        requisition_fieldset,
        requisition_status_fieldset,
        requisition_identifier_fieldset,
        audit_fieldset_tuple)

    radio_fields = {
        'is_drawn': admin.VERTICAL,
        'reason_not_drawn': admin.VERTICAL,
        'item_type': admin.VERTICAL,
    }

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj)
                + requisition_identifier_fields)
