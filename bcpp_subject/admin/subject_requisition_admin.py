from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..models import SubjectRequisition

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(SubjectRequisition, site=bcpp_subject_admin)
class SubjectRequisitionAdmin (CrfModelAdminMixin, admin.ModelAdmin):

    pass
