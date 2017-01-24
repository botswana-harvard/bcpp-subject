from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..models import SubjectRequisition
from ..forms import SubjectRequisitionForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SubjectRequisition, site=bcpp_subject_admin)
class SubjectRequisitionAdmin (CrfModelAdminMixin, admin.ModelAdmin):

    form = SubjectRequisitionForm

    radio_fields = {
        'is_drawn': admin.VERTICAL,
        'reason_not_drawn': admin.VERTICAL,
        'item_type': admin.VERTICAL,
    }
