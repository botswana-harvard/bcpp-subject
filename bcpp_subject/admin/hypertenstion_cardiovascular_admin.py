from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..models import HypertensionCardiovascular


@admin.register(HypertensionCardiovascular, site=bcpp_subject_admin)
class HypertensionCardiovascularAdmin(admin.ModelAdmin):

    radio_fields = {
        "may_take_blood_pressure": admin.VERTICAL,
        "hypertension_diagnosis": admin.VERTICAL,
        "medications_taken": admin.VERTICAL,
        "is_medication_still_given": admin.VERTICAL,
        "health_care_facility": admin.VERTICAL,
        "salt_intake_counselling": admin.VERTICAL,
        "tobacco_smoking": admin.VERTICAL,
        "tobacco_counselling": admin.VERTICAL,
        "weight_counselling": admin.VERTICAL,
        "physical_activity_counselling": admin.VERTICAL,
        "alcohol_counselling": admin.VERTICAL,
        "blood_test_for_cholesterol": admin.VERTICAL,
        "blood_test_for_diabetes": admin.VERTICAL}
