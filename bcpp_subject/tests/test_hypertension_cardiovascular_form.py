from django.test import TestCase

from ..forms import HypertensionCardiovascularForm


class TestHypertensionCardiovascular(TestCase):

    def setUp(self):
        """Initial data set to valid"""
        self.data = {
            'may_take_blood_pressure': 'No',
            'hypertension_diagnosis': None,
            'medications_taken': None,
            'if_other': None,
            'medication_still_given': None,
            'if_other_given_medication_given': None,
            'health_care_facility': None,
            'salt_intake_counselling': None,
            'tobacco_smoking': None,
            'tobacco_counselling': None,
            'weight_counselling': None,
            'physical_activity_counselling': None,
            'alcohol_counselling': None,
            'blood_test_for_cholesterol': None,
            'blood_test_for_diabetes': None}

    def test_valid_form(self):
        """Test to verify whether form will submit"""
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertTrue(form.is_valid())
