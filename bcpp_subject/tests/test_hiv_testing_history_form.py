from django.test import TestCase

from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, POS, NEG, DWTA, NOT_APPLICABLE

from ..forms import HivTestingHistoryForm

from .test_mixins import SubjectMixin


class TestHivTestingHistoryForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')
        self.options = {
            'report_datetime': get_utcnow(),
            'subject_visit': self.subject_visit.id,
            'has_tested': YES,
            'when_hiv_test': '1 to 5 months ago',
            'has_record': YES,
            'verbal_hiv_result': POS,
            'other_record': YES,
        }

    def test_form_is_valid(self):
        """test hiv_tested form fields are valid"""
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertTrue(hiv_testing_history_form.is_valid())

    def test_validate_prior_hiv(self):
        """test if there was prior hiv test since last visit"""
        self.options.update(has_tested=NO)
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertFalse(hiv_testing_history_form.is_valid())

    def test_has_tested_without_when_hiv(self):
        """ test if hiv test date was provided"""
        self.options.update(when_hiv_test=None)
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertFalse(hiv_testing_history_form.is_valid())

    def test_has_tested_without_record(self):
        """test if subject has tested, record was provided"""
        self.options.update(has_record=None)
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertFalse(hiv_testing_history_form.is_valid())

    def test_validate_prior_hiv_DWTA(self):
        """test if there was prior hiv test since last visit"""
        self.options.update(has_tested=DWTA)
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertFalse(hiv_testing_history_form.is_valid())

    def test_hiv_neg_with_other_record(self):
        """test if hiv negative with other records is invalid"""
        self.options.update(verbal_hiv_result=NEG)
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertFalse(hiv_testing_history_form.is_valid())

    def test_hiv_pos_without_other_record(self):
        """test if other records were provided for hiv positive subject"""
        self.options.update(other_record=NOT_APPLICABLE)
        hiv_testing_history_form = HivTestingHistoryForm(data=self.options)
        self.assertFalse(hiv_testing_history_form.is_valid())
