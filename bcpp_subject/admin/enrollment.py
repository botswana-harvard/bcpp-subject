from django.contrib import admin
from django.urls.base import reverse

from edc_base.modeladmin_mixins import audit_fieldset_tuple, audit_fields

from ..admin_site import bcpp_subject_admin

from ..models.enrollment import Enrollment

from .modeladmin_mixins import ModelAdminMixin


@admin.register(Enrollment, site=bcpp_subject_admin)
class EnrollmentAdmin(ModelAdminMixin, admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ("subject_identifier", 'report_datetime', 'survey')}),
        audit_fieldset_tuple)

    readonly_fields = ("subject_identifier", 'report_datetime', 'survey')

    list_display = ("subject_identifier", 'report_datetime', 'survey')

    list_filter = ('report_datetime', 'survey')

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj) + audit_fields

    def view_on_site(self, obj):
        return reverse(
            'bcpp-subject:dashboard_url', kwargs=dict(
                subject_identifier=obj.subject_identifier,
                survey=obj.survey))
