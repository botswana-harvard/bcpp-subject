from django.test import TestCase, tag
from datetime import date

from edc_constants.constants import YES

from ..forms import CircumcisedForm
from .test_mixins import SubjectMixin


class TestCircumcisedForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.make_subject_visit_for_consented_subject('T0')

        self.options = {
            'circumcised': YES,
            'circ_date': date.today(),
            'when_circ': 18,
            'age_unit_circ': 'Years',
            'where_circ': 'Government clinic or hospital',
            'why_circ': 'Improved hygiene',
        }

    def test_circumcision_health_benefits_smc_none(self):
        self.options.update(health_benefits_smc=None)
        form = CircumcisedForm(data=self.options)
        self.assertFalse(form.is_valid())
