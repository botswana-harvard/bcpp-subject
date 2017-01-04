from datetime import date, timedelta

from django.test import TestCase

from edc_base.utils import get_utcnow

from ..forms import HivTestReviewForm

from .test_mixins import SubjectMixin

from edc_constants.choices import NEG


class TestHivTestReviewForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject(
            'T0')
        yesterday = date.today() - timedelta(1)

        self.options = {
           'subject_visit': self.subject_visit.id,
           'report_datetime': get_utcnow(),
           'hiv_test_date': yesterday,
           'recorded_hiv_result': NEG,
         }

    def test_form_is_valid(self):
        form = HivTestReviewForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_date_tested_hiv(self):
        """The HIV test date cannot be equal to today\'s date or tomorow's date,
         otherwise Throw Validation error"""
        form = HivTestReviewForm(data=self.options)
        self.options.update(hiv_test_date=date.today())
        self.assertFalse(form.is_valid())

        self.options.update(hiv_test_date=(date.today() + timedelta(1)))
        self.assertFalse(form.is_valid())
