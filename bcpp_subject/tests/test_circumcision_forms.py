from django.test import TestCase, tag
from datetime import date
import arrow

from edc_constants.constants import YES

from ..forms import CircumcisedForm, UncircumcisedForm
from .test_mixins import SubjectMixin
from bcpp_subject.models.list_models import CircumcisionBenefits


class TestCircumcisedForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        subject_visit = self.make_subject_visit_for_consented_subject('T0')

        health_benefits_smc = CircumcisionBenefits.objects.create(name='Improved hygiene')

        self.options = {
            'circumcised': YES,
            'circ_date': arrow.utcnow().date(),
            'report_datetime': self.get_utcnow(),
            'when_circ': 18,
            'subject_visit': subject_visit.id,
            'age_unit_circ': 'Years',
            'where_circ': 'Government clinic or hospital',
            'why_circ': 'Improved hygiene',
            'health_benefits_smc': [health_benefits_smc.id]
        }

    def test_circumcision_form_valid(self):
        form = CircumcisedForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_circumcision_health_benefits_smc_none(self):
        self.options.update(health_benefits_smc=None)
        form = CircumcisedForm(data=self.options)
        self.assertFalse(form.is_valid())


class TestUncircumcisedForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        subject_visit = self.make_subject_visit_for_consented_subject('T0')
        health_benefits_smc = CircumcisionBenefits.objects.create(name='Improved hygiene')

        self.options = {
            'circumcised': YES,
            'report_datetime': self.get_utcnow(),
            'subject_visit': subject_visit.id,
            'reason_circ': 'Circumcision never offered to me',
            'future_circ': YES,
            'future_reasons_smc': 'More information about benefits',
            'service_facilities': YES,
            'aware_free': 'Radio',
            'health_benefits_smc': [health_benefits_smc.id]
        }

    def test_uncircumcision_form_valid(self):
        form = UncircumcisedForm(data=self.options)
        print(form.errors)
#         self.assertTrue(form.is_valid())
#         print(form.errors.get("__all__"))

    def test_uncircumcision_health_benefits_smc_none(self):
        self.options.update(health_benefits_smc=None)
        form = UncircumcisedForm(data=self.options)
        self.assertFalse(form.is_valid())
