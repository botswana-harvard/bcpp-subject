from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import HivTestReviewForm
from ..models import HivTestReview

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivTestReview, site=bcpp_subject_admin)
class HivTestReviewAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HivTestReviewForm

    fieldsets = (
        (None, {
            'fields': (
                "subject_visit",
                'hiv_test_date',
                'recorded_hiv_result')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        "recorded_hiv_result": admin.VERTICAL, }

    additional_instructions = (
        'Answer the following about the record of the last most recent HIV test')
