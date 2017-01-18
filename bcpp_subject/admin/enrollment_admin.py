from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch

from edc_base.modeladmin_mixins import audit_fieldset_tuple, audit_fields

from ..admin_site import bcpp_subject_admin
from ..models import EnrollmentBhs, EnrollmentAhs, EnrollmentEss

from .modeladmin_mixins import ModelAdminMixin


class Mixin:

    fieldsets = (
        (None, {
            'fields': ("subject_identifier", 'report_datetime', 'survey')}),
        audit_fieldset_tuple)

    readonly_fields = ("subject_identifier", 'report_datetime', 'survey')

    list_display = ("subject_identifier", 'report_datetime', 'survey')

    list_filter = ('report_datetime', 'survey', 'survey_schedule')

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj) + audit_fields

    def view_on_site(self, obj):
        try:
            return reverse(
                'bcpp-subject:dashboard_url', kwargs=dict(
                    subject_identifier=obj.subject_identifier,
                    survey=obj.survey_object.field_value,
                    survey_schedule=obj.survey_object.survey_schedule.field_value))
        except NoReverseMatch:
            return super().view_on_site(obj)


@admin.register(EnrollmentBhs, site=bcpp_subject_admin)
class EnrollmentBhsAdmin(Mixin, ModelAdminMixin, admin.ModelAdmin):

    pass


@admin.register(EnrollmentAhs, site=bcpp_subject_admin)
class EnrollmentAhsAdmin(Mixin, ModelAdminMixin, admin.ModelAdmin):

    pass


@admin.register(EnrollmentEss, site=bcpp_subject_admin)
class EnrollmentEssAdmin(Mixin, ModelAdminMixin, admin.ModelAdmin):

    pass
