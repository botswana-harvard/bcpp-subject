from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple, audit_fields
from edc_lab.admin_site import edc_lab_admin

from ...models import Result
from ..modeladmin_mixins import ModelAdminMixin
from .result_item_admin import ResultItemInlineAdmin


@admin.register(Result, site=edc_lab_admin)
class ResultAdmin(ModelAdminMixin, admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': (
                'requisition',
                'panel_name',
                'report_datetime',
            )}),
        ('Status', {
            'fields': (
                'pending',
                'pending_datetime',
                'resulted',
                'resulted_datetime',
            )}),
        audit_fieldset_tuple)

    inlines = [ResultItemInlineAdmin]

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj=obj) + audit_fields
