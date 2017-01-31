from django.test.testcases import TestCase
from bcpp_subject.tests.test_mixins import SubjectMixin
from edc_constants.constants import YES, NO
from bcpp_subject.forms.resource_utilization_form import ResourceUtilizationForm


class TestResourceUtilizationForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.options = {
            'out_patient': YES,
            'hospitalized': 3,
            'money_spent': 3000.00,
            'medical_cover': YES,
            'subject_visit': self.subject_visit_male.id,
            'report_datetime': self.get_utcnow(),
        }

    def test_form_valid(self):
        form = ResourceUtilizationForm(data=self.options)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save)

    def test_if_money_spent_is_not_medical_aid_cover(self):
        """Assert that money spent was not from the medical aid cover"""
        self.options.update(money_spent=3000.00, medical_cover=NO)
        form = ResourceUtilizationForm(data=self.options)
        self.assertTrue(form.is_valid())

        self.options.update(money_spent=3000.00, medical_cover=None)
        form = ResourceUtilizationForm(data=self.options)
        self.assertFalse(form.is_valid())
