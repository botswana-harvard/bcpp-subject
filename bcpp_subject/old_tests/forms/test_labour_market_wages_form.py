from django.test import TestCase

from edc_constants.constants import NO

from ..forms import LabourMarketWagesForm
from .test_mixins import SubjectMixin


class TestLabourMarketWagesForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()

        self.options = {
            'report_datetime': self.get_utcnow(),
            'subject_visit': self.subject_visit_male.id,
            'employed': 'government sector',
            'occupation': 'Mining',
            'job_description_change': None,
            'days_worked': 5,
            'monthly_income': '500-999 pula',
            'salary_payment': 'Fixed salary',
            'household_income': '1000-4999 pula',
            'other_occupation': 'Studying',
            'govt_grant': NO,
            'nights_out': None,
            'weeks_out': NO,
            'days_not_worked': None,
            'days_inactivite': None,
        }

    def test_form_is_valid(self):
        form = LabourMarketWagesForm(data=self.options)
        self.assertTrue(form.is_valid())
