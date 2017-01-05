from django.test import TestCase

from edc_constants.constants import YES, NO

from ..constants import NOT_SURE
from ..forms import HivUntestedForm

from .test_mixins import SubjectMixin


class TestHivUntestedForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')
        self.options = {
            'report_datetime': self.get_utcnow(),
            'why_no_hiv_test': 'I recently tested',
            'hiv_pills': YES,
            'arvs_hiv_test': YES,
            'subject_visit': self.subject_visit.id,
        }

    def test_form_is_valid(self):
        hiv_untested_form = HivUntestedForm(data=self.options)
        self.assertTrue(hiv_untested_form.is_valid())

    def test_no_hiv_pills_none_arvs_hiv(self):
        """Assert information about ARV was provided without having heard of ARV's."""
        self.options.update(hiv_pills=NO)
        hiv_untested_form = HivUntestedForm(data=self.options)
        self.assertFalse(hiv_untested_form.is_valid())

    def test_hiv_pills_none_arvs_hiv(self):
        """Assert information about ARV was not provided without, heard of ARV's."""
        self.options.update(arvs_hiv_test=None)
        hiv_untested_form = HivUntestedForm(data=self.options)
        self.assertFalse(hiv_untested_form.is_valid())

    def test_not_sure_hiv_pills_none_arvs_hiv(self):
        """Assert information about ARV was not provided without being sure of having heard of ARV's."""
        self.options.update(hiv_pills=NOT_SURE, arvs_hiv_test=None)
        hiv_untested_form = HivUntestedForm(data=self.options)
        self.assertFalse(hiv_untested_form.is_valid())
