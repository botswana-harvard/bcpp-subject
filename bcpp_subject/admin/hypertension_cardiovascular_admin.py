from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple, audit_fields

from ..admin_site import bcpp_subject_admin
from ..forms import HypertensionCardiovascularForm
from ..models import HypertensionCardiovascular
from .modeladmin_mixins import ModelAdminMixin


@admin.register(HypertensionCardiovascular, site=bcpp_subject_admin)
class HypertensionCardiovascularAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = HypertensionCardiovascularForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'may_take_blood_pressure',
                'hypertension_diagnosis',
                'medication_taken',
                'other_medication_taken',
                'medication_given',
                'other_medication_given',
                'health_care_facility',
                'salt_intake_counselling',
                'tobacco_smoking',
                'tobacco_counselling',
                'weight_history'
                'weight_counselling',
                'physical_activity_counselling',
                'alcohol_counselling',
                'blood_test_for_cholesterol',
                'blood_test_for_diabetes')
        }),
        ('Blood Pressure Measurement', {
            'fields': (
                'right_arm_one',
                'left_arm_one',
                'right_arm_two',
                'left_arm_two')
        }),
        ('Waist Circumference Measurement', {
            'fields': (
                'waist_reading_one',
                'waist_reading_two',
                'hip_reading_one',
                'hip_reading_two')
        }),
        audit_fieldset_tuple,
    )

    filter_horizontal = (
        'medication_taken',
        'medication_given')

    radio_fields = {
        'may_take_blood_pressure': admin.VERTICAL,
        'hypertension_diagnosis': admin.VERTICAL,
        'health_care_facility': admin.VERTICAL,
        'salt_intake_counselling': admin.VERTICAL,
        'tobacco_smoking': admin.VERTICAL,
        'tobacco_counselling': admin.VERTICAL,
        'weight_counselling': admin.VERTICAL,
        'physical_activity_counselling': admin.VERTICAL,
        'alcohol_counselling': admin.VERTICAL,
        'blood_test_for_cholesterol': admin.VERTICAL,
        'blood_test_for_diabetes': admin.VERTICAL,
        'weight_history': admin.VERTICAL}

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj) + audit_fields
