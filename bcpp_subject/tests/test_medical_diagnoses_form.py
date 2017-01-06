from django.test import TestCase

from edc_constants.constants import NO, YES

from model_mommy import mommy

from ..forms import MedicalDiagnosesForm

from .test_mixins import SubjectMixin


class TestMedicalDiagnosesForm(SubjectMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')
        self.diagnoses1 = mommy.make_recipe('bcpp_subject.diagnoses', name='Heart Disease or Stroke')
        self.options = {
            'heart_attack_record': YES,
            'cancer_record': None,
            'diagnoses': [self.diagnoses1.id],
            'tb_record': None,
            'subject_visit': self.subject_visit.id,
            'report_datetime': self.get_utcnow(),
        }

    def test_valid_form(self):
        form = MedicalDiagnosesForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_if_previous_diagnoses_has_been_provided(self):
        """Asserts that previous diagnoses has been provided"""
        self.options.update(diagnoses=None)
        form = MedicalDiagnosesForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_to_check_if_diagnoses_has_been_made(self):
        """Asserts that diagnoses has been made or none performed"""
#        self.diagnoses1 = mommy.make_recipe('bcpp_subject.diagnoses', name = 'Heart Disease or Stroke')
        self.options.update(diagnoses=[None, self.diagnoses1])
        form = MedicalDiagnosesForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_participant_has_had_heart_attack(self):
        """Asserts that participant has had heart attack"""
        self.options.update(heart_attack_record=None)
        form = MedicalDiagnosesForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_participant_has_cancer(self):
        """Asserts that participant has been diagnosed with cancer"""
        self.diagnoses2 = mommy.make_recipe('bcpp_subject.diagnoses', name='Cancer')
        self.options.update(cancer_record=None, diagnoses=[self.diagnoses2.id])
        form = MedicalDiagnosesForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_participant_has_been_diagnosed_tubercolosis(self):
        """Asserts that participant has been diagnosed with Tubercolosis"""
        self.diagnoses3 = mommy.make_recipe('bcpp_subject.diagnoses', name='Tubercolosis')
        self.diagnoses3.save()
        self.options.update(tb_record=None, diagnoses=[self.diagnoses3.id])
        form = MedicalDiagnosesForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_any_diagnoses_has_been_done(self):
        """Asserts that no diagnoses has been done"""
        self.options.update(diagnoses=None)
        self.options.update(heart_attack_record=NO, cancer_record=NO, tb_record=NO)
        form = MedicalDiagnosesForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_diagnosis_list_is_empty(self):
        """Asserts that if diagnosis list is empty then no records should exist"""
        self.options.update(diagnoses=None)
        self.options.update(heart_attack_record=YES, cancer_record=YES, tb_record=YES)
        form = MedicalDiagnosesForm(data=self.options)
        self.assertFalse(form.is_valid())
