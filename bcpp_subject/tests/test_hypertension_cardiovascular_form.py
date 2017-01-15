from django.test import TestCase

from ..forms import HypertensionCardiovascularForm
from .test_mixins import SubjectMixin


class TestHypertensionCardiovascular(SubjectMixin, TestCase):

    def setUp(self):
        """Initial data set to valid"""
        super().setUp()
        subject_visit = self.make_subject_visit_for_consented_subject('T0')
        self.data = {
            'may_take_blood_pressure': 'No',
            'hypertension_diagnosis': None,
            'medications_taken': None,
            'if_other_medications_taken': None,
            'medication_still_given': None,
            'if_other_medication_still_given': None,
            'health_care_facility': None,
            'salt_intake_counselling': None,
            'tobacco_smoking': None,
            'tobacco_counselling': None,
            'weight_counselling': None,
            'physical_activity_counselling': None,
            'alcohol_counselling': None,
            'blood_test_for_cholesterol': None,
            'blood_test_for_diabetes': None,
            'subject_visit': subject_visit.id,
            'report_datetime': self.get_utcnow()}

    def test_valid_form(self):
        """Test to verify whether form will submit"""
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_bp_not_measured_fields_filled_hypertension_diagnosis(self):
        """Test to verify validation works when participant doesn't \
        want to get weight/BP measured, but hypertension diagnoses \
        question is answered"""
        self.data['hypertension_diagnosis'] = 'Yes'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_bp_not_measured_fields_filled_health_care_facility(self):
        """Test to verify validation works when participant doesn't \
        want to get weight/BP measured, but health_care_facility \
        question is answered"""
        self.data['health_care_facility'] = 'clinic'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_bp_not_measured_fields_filled_if_other_medications_taken(self):
        """Test to verify validation works when participant doesn't \
        want to get weight/BP measured, but if_other_medications_taken \
        question is answered"""
        self.data['if_other_medications_taken'] = 'Some medication'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_bp_not_measured_fields_filled_salt_intake_counselling(self):
        """Test to verify validation works when participant doesn't \
        want to get weight/BP measured, but salt_intake_counselling \
        question is answered"""
        self.data['salt_intake_counselling'] = 'No'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_bp_not_measured_fields_filled_salt_tobacco_smoking(self):
        """Test to verify validation works when participant doesn't \
        want to get weight/BP measured, but salt_tobacco_smoking \
        question is answered"""
        self.data['tobacco_smoking'] = 'Yes'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_bp_not_measured_fields_filled_salt_tobacco_counselling(self):
        """Test to verify validation works when participant doesn't \
        want to get weight/BP measured, but tobacco_counselling \
        question is answered"""
        self.data['tobacco_counselling'] = 'Yes'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_bp_not_measured_fields_filled_weight_counselling(self):
        """Test to verify validation works when participant doesn't \
        want to get weight/BP measured, but weight_counselling \
        question is answered"""
        self.data['weight_counselling'] = 'Yes'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_bp_not_measured_fields_filled_physical_activity_counselling(self):
        """Test to verify validation works when participant doesn't \
        want to get weight/BP measured, but physical_activity_counselling \
        question is answered"""
        self.data['physical_activity_counselling'] = 'Yes'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_bp_not_measured_fields_filled_alcohol_counselling(self):
        """Test to verify validation works when participant doesn't \
        want to get weight/BP measured, but alcohol_counselling \
        question is answered"""
        self.data['alcohol_counselling'] = 'Yes'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_bp_not_measured_fields_filled_blood_test_for_cholesterol(self):
        """Test to verify validation works when participant doesn't \
        want to get weight/BP measured, but blood_test_for_cholesterol \
        question is answered"""
        self.data['blood_test_for_cholesterol'] = 'Yes'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_bp_not_measured_fields_filled_blood_test_for_diabetes(self):
        """Test to verify validation works when participant doesn't \
        want to get weight/BP measured, but blood_test_for_cholesterol \
        question is answered"""
        self.data['blood_test_for_diabetes'] = 'No'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())
