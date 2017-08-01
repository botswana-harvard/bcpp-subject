from django.test import TestCase

from edc_constants.constants import YES

from ..forms import HospitalAdmissionForm
from .test_mixins import SubjectMixin


class TestHospitalAdmissionForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.consent_data = {
            'identity': '31721515',
            'confirm_identity': '31721515',
            'report_datetime': self.get_utcnow(),
        }
        self.bhs_subject_visit_male = (
            self.make_subject_visit_for_consented_subject_male('E0', **self.consent_data))
        self.options = {
            'subject_visit': self.bhs_subject_visit_male.id,
            'report_datetime': self.get_utcnow(),
            'admission_nights': 2,
            'reason_hospitalized': 'Pregnancy',
            'facility_hospitalized': 'Clinic',
            'nights_hospitalized': 2,
            'healthcare_expense': 100.00,
            'travel_hours': '1 to under 2 hours',
            'total_expenses': 100.00,
            'hospitalization_costs': YES,
        }

    def test_form_is_valid(self):
        form = HospitalAdmissionForm(data=self.options)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_zero_admission_nights_with_reason_hospitalized(self):
        """Asserts zero admission nights must have
        none hospitalization reason"""
        self.options.update(admission_nights=0, reason_hospitalized=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_zero_admission_nights_with_travel_hours(self):
        """Asserts zero admission nights must have
        none travel hours"""
        self.options.update(admission_nights=0, travel_hours=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_zero_admission_nights_with_hospitalization_costs(self):
        """Asserts zero admission nights must have
        none hospitalization_costs"""
        self.options.update(admission_nights=0, hospitalization_costs=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_admission_nights_value_gt_zero_none_reason_hospitalized(self):
        """Asserts zero admission nights must have
        none reason_hospitalized"""
        self.options.update(admission_nights=0, reason_hospitalized=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_admission_nights_value_gt_zero_none_travel_hours(self):
        """Asserts zero admission nights must have travel_hours"""
        self.options.update(admission_nights=0, travel_hours=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_admission_nights_value_gt_zero_none_facility_hospitalized(self):
        """Asserts admission nights must have facility_hospitalized"""
        self.options.update(facility_hospitalized=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_admission_nights_value_gt_zero_none_nights_hospitalized(self):
        """Asserts admission nights must have nights_hospitalized"""
        self.options.update(nights_hospitalized=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_healthcare_expense_gt_hospitalization_costs(self):
        """Asserts healthcare_expense must have hospitalization_costs"""
        self.options.update(hospitalization_costs=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_total_expenses_gt_hospitalization_costs(self):
        """Asserts total_expenses must have hospitalization_costs"""
        self.options.update(hospitalization_costs=None)
        form = HospitalAdmissionForm(data=self.options)
        self.assertFalse(form.is_valid())
