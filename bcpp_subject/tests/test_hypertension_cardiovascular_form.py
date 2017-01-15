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
        self.data['hypertension_diagnosis'] = 'No'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_bp_not_measured_fields_filled_health_care_facility(self):
        """Test to verify validation works when participant doesn't \
        want to get weight/BP measured, but health_care_facility \
        question is answered"""
        self.data['health_care_facility'] = 'Clinic'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.data['health_care_facility'] = 'Primary Hospital'
        form = HypertensionCardiovascularForm(data=self.data)
        self.assertFalse(form.is_valid())
