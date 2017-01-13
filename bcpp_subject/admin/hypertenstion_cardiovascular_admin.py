from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple, audit_fields

from ..admin_site import bcpp_subject_admin
from ..forms import HypertensionCardiovascularForm
from ..models import HypertensionCardiovascular, BPMeasurement, WaistCircumferenceMeasurement
from .modeladmin_mixins import ModelAdminMixin


class BPMeasurementAdmin(admin.StackedInline):

    model = BPMeasurement

    fieldsets = (
        (None, {
            'fields': (
                'bp_measurement',
                'time_zero',
                'right_arm_one',
                'left_arm_one',
                'right_arm_two',
                'left_arm_two')
        }),
    )


class WaistCircumferenceMeasurement(admin.StackedInline):

    model = WaistCircumferenceMeasurement

    fieldsets = (
        (None, {
            'fields': (
                'waist_circumference_measurement',
                'waist_reading_one',
                'waist_reading_two',
                'hip_reading_one',
                'hip_reading_two')
        }),
    )


@admin.register(HypertensionCardiovascular, site=bcpp_subject_admin)
class HypertensionCardiovascularAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = HypertensionCardiovascularForm

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
        'blood_test_for_diabetes': admin.VERTICAL}

    fieldsets = (
        (None, {
            'fields': (
                'may_take_blood_pressure',
                'hypertension_diagnosis',
                'medications_taken',
                'if_other',
                'is_medication_still_given',
                'if_other_given_medication_given',
                'health_care_facility',
                'salt_intake_counselling',
                'tobacco_smoking',
                'tobacco_counselling',
                'weight_counselling',
                'physical_activity_counselling',
                'alcohol_counselling',
                'blood_test_for_cholesterol',
                'blood_test_for_diabetes')
        }),
        audit_fieldset_tuple,
    )

    inlines = (BPMeasurementAdmin, WaistCircumferenceMeasurement)

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj) + audit_fields
