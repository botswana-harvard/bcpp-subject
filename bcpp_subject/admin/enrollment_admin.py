from edc_base.modeladmin_mixins import audit_fieldset_tuple, audit_fields
from edc_visit_schedule.admin import (
    visit_schedule_only_fieldset_tuple, visit_schedule_only_fields)

from survey.admin import survey_fieldset_tuple, survey_fields

from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch

from ..admin_site import bcpp_subject_admin
from ..models import Enrollment
from .modeladmin_mixins import ModelAdminMixin


@admin.register(Enrollment, site=bcpp_subject_admin)
class EnrollmentAdmin(ModelAdminMixin, admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'report_datetime')}),
        visit_schedule_only_fieldset_tuple,
        survey_fieldset_tuple,
        audit_fieldset_tuple)

    readonly_fields = ('subject_identifier', 'report_datetime', 'survey')

    list_display = ('subject_identifier', 'report_datetime', 'survey')

    list_filter = ('report_datetime', 'survey', 'survey_schedule')

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj)
                + audit_fields
                + survey_fields
                + visit_schedule_only_fields)

    def view_on_site(self, obj):
        try:
            return reverse(
                'bcpp-subject:dashboard_url', kwargs=dict(
                    subject_identifier=obj.subject_identifier,
                    household_identifier=(
                        obj.household_member.household_structure.
                        household.household_identifier),
                    survey=obj.survey_object.field_value,
                    survey_schedule=obj.survey_object.survey_schedule.field_value))
        except NoReverseMatch:
            return super().view_on_site(obj)
