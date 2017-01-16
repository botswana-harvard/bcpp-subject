from django.test import TestCase

from edc_constants.constants import YES, NO, POS, NEG, DWTA, NOT_APPLICABLE

from ..forms import HivTestingHistoryForm

from .test_mixins import SubjectMixin


class TestHivTestingHistoryForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.consent_data = {
            'identity': '31721515',
            'confirm_identity': '31721515',
        }
        self.bhs_subject_visit_female = self.make_subject_visit_for_consented_subject_female('T0', **self.consent_data)
        self.options = {
            'report_datetime': self.get_utcnow(),
            'subject_visit': self.bhs_subject_visit_female.id,
            'has_tested': YES,
            'when_hiv_test': '1 to 5 months ago',
            'has_record': YES,
            'verbal_hiv_result': POS,
            'other_record': YES,
        }

    def test_form_is_valid(self):
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertTrue(hiv_testing_history_form.is_valid())
        self.assertTrue(hiv_testing_history_form.save())

    def test_validate_prior_hiv_test(self):
        self.options.update(has_tested=NO)
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertFalse(hiv_testing_history_form.is_valid())

    def test_validate_prior_hiv_DWTA(self):
        """Assert other fields provided only if prior hiv test"""
        self.options.update(has_tested=DWTA)
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertFalse(hiv_testing_history_form.is_valid())

    def test_has_tested_without_hiv_date(self):
        self.options.update(when_hiv_test=None)
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertFalse(hiv_testing_history_form.is_valid())

    def test_has_tested_without_record(self):
        self.options.update(has_record=None)
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertFalse(hiv_testing_history_form.is_valid())

    def test_hiv_neg_with_other_record(self):
        """Assert if hiv negative with other records is invalid"""
        self.options.update(verbal_hiv_result=NEG)
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertFalse(hiv_testing_history_form.is_valid())

    def test_hiv_pos_without_other_record(self):
        """Assert if other records were provided for hiv positive subject"""
        self.options.update(other_record=NOT_APPLICABLE)
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertFalse(hiv_testing_history_form.is_valid())
