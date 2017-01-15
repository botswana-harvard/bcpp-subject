from django.test import TestCase

from edc_constants.constants import YES, NO

from ..constants import NOT_SURE
from ..forms import HivTestedForm

from .test_mixins import SubjectMixin


class TestHivTestedForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')
        self.options = {
            'report_datetime': self.get_utcnow(),
            'num_hiv_tests': 1,
            'where_hiv_test': 'Tebelopele VCT center',
            'why_hiv_test': 'I was worried I might have HIV and wanted to know my status',
            'hiv_pills': YES,
            'arvs_hiv_test': YES,
            'subject_visit': self.subject_visit.id,
        }

    def test_form_is_valid(self):
        hiv_tested_form = HivTestedForm(data=self.options)
        self.assertTrue(hiv_tested_form.is_valid())
        self.assertTrue(hiv_tested_form.save())

    def test_num_hiv_valid(self):
        """Assert number of hiv tests was not provided."""
        self.options.update(num_hiv_tests=0)
        hiv_tested_form = HivTestedForm(data=self.options)
        self.assertFalse(hiv_tested_form.is_valid())

    def test_no_hiv_pills_with_arvs_hiv_invalid(self):
        """Assert information about ARV was provided but not having heard of ARV's."""
        self.options.update(hiv_pills=NO)
        hiv_tested_form = HivTestedForm(data=self.options)
        self.assertFalse(hiv_tested_form.is_valid())

    def test_hiv_pills_none_arvs_hiv_invalid(self):
        """Assert information about ARV was not provided, having heard of ARV's."""
        self.options.update(arvs_hiv_test=None)
        hiv_tested_form = HivTestedForm(data=self.options)
        self.assertFalse(hiv_tested_form.is_valid())

    def test_not_sure_hiv_pills_none_arvs_hiv_test(self):
        """Assert information about ARV was not provided without being sure of having heard of ARV's."""
        self.options.update(hiv_pills=NOT_SURE, arvs_hiv_test=None)
        hiv_tested_form = HivTestedForm(data=self.options)
        self.assertFalse(hiv_tested_form.is_valid())
