from django.test import TestCase
from model_mommy import mommy

from ..forms import DemographicsForm
from .test_mixins import SubjectMixin
from django.forms.forms import Form


class TestDemographicsForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.consent_data = {
            'identity': '31721515',
            'confirm_identity': '31721515',
            'report_datetime': self.get_utcnow(),
        }
        self.bhs_subject_visit_female = self.make_subject_visit_for_consented_subject_female('E0', **self.consent_data)

        self.religion = mommy.make_recipe('bcpp_subject.religion')
        self.ethics = mommy.make_recipe('bcpp_subject.ethnicgroups')
        self.livewith = mommy.make_recipe('bcpp_subject.livewith')

        self.data = {
            'ethnic_other': '',
            'husband_wives': None,
            'marital_status': 'Widowed',
            'report_datetime': self.get_utcnow(),
            'num_wives': None,
            'live_with': [self.livewith.id],
            'religion': [self.religion.id],
            'religion_other': u'',
            'subject_visit': self.bhs_subject_visit_female.id,
            'ethnic': [self.ethics.id]
        }

    def test_demographics_form_valid(self):
        form = DemographicsForm(data=self.data)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_marriage_gender_female_valid(self):
        """ Assert that is a participant is married and with number of wife less than zero validation error thrown"""
        self.data.update(num_wives=0, husband_wives=0, marital_status='Married')
        form = DemographicsForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_live_with_alone_valid(self):
        """ Assert that the many to many Alone can not be selected with another value."""
        livewith2 = mommy.make_recipe('bcpp_subject.livewith', name='Alone', short_name='Alone')
        self.data.update(live_with=[self.livewith.id, livewith2.id])
        form = DemographicsForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_live_with_don_not_want_to_answer_valid(self):
        """ Assert that the many to many Don\'t want to answer can not be selected with another value."""
        livewith2 = mommy.make_recipe('bcpp_subject.livewith', name='Don\'t want to answer', short_name='Don\'t want to answer')
        self.data.update(live_with=[self.livewith.id, livewith2.id])
        form = DemographicsForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_1_ethic_group_at_a_time(self):
        """ Assert that a participant can only be in 1 ethenic group."""
        ethnic2 = mommy.make_recipe('bcpp_subject.ethnicgroups', name='Bakgatla', short_name='Bakgatla')
        self.data.update(ethnic=[self.ethics.id, ethnic2.id])
        form = DemographicsForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_1_religion_group_at_a_time(self):
        """ Assert that a participant can only be in 1 religion."""
        religion2 = mommy.make_recipe('bcpp_subject.ethnicgroups', name='ZCC', short_name='ZCC')
        self.data.update(religion=[self.religion.id, religion2.id])
        form = DemographicsForm(data=self.data)
        self.assertFalse(form.is_valid())

    def test_unmarried_has_no_wives(self):
        """Assert that a unmarried participant can not have wives."""
        self.consent_data = {
            'identity': '31721516',
            'confirm_identity': '31721516',
            'report_datetime': self.get_utcnow(),
        }
        self.bhs_subject_visit_male = self.make_subject_visit_for_consented_subject_male('E0', **self.consent_data)
        self.data.update(marital_status='Single/never married', num_wives=3, subject_visit=self.bhs_subject_visit_male.id)
        form = DemographicsForm(data=self.data)
        self.assertFalse(form .is_valid())

    def test_unmarried_has_no_husbands(self):
        """Assert that an unmarried participant can not have husbands."""
        self.data.update(marital_status='Single/never married', num_wives=None, husband_wives=3)
        form = DemographicsForm(data=self.data)
        self.assertFalse(form .is_valid())

    def test_marital_status_wives(self):
        """Assert that if married and the participant is male the number of wife has to be greater than 1."""
        self.consent_data = {
            'identity': '31721517',
            'confirm_identity': '31721517',
            'report_datetime': self.get_utcnow(),
        }
        self.bhs_subject_visit_male = self.make_subject_visit_for_consented_subject_male('E0', **self.consent_data)
        self.data.update(marital_status='Married', num_wives=0, husband_wives=0, subject_visit=self.bhs_subject_visit_male.id)
        form = DemographicsForm(data=self.data)
        self.assertFalse(form .is_valid())

    def test_marital_status_husbands(self):
        """Assert that if married and the participant is female the number of husband has to be greater than 1."""
        self.data.update(marital_status='Married', husband_wives=0)
        form = DemographicsForm(data=self.data)
        self.assertFalse(form .is_valid())

    def test_married_woman_has_husband_null_wives(self):
        """Assert that if married and the participant is woman
                        should allow null wives"""
        self.consent_data = {
            'identity': '31721517',
            'confirm_identity': '31721517',
            'report_datetime': self.get_utcnow(),
        }
        self.bhs_subject_visit_female = self.make_subject_visit_for_consented_subject_female('E0', **self.consent_data)
        self.data.update(marital_status='Married', num_wives=None, husband_wives=1, subject_visit=self.bhs_subject_visit_female.id)
        form = DemographicsForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_married_man_has_wives_null_husbands(self):
        """Assert that if married and the participant is man
                        should allow null husbands"""
        self.consent_data = {
            'identity': '31721517',
            'confirm_identity': '31721517',
            'report_datetime': self.get_utcnow(),
        }
        self.bhs_subject_visit_male = self.make_subject_visit_for_consented_subject_male('E0', **self.consent_data)
        self.data.update(marital_status='Married', num_wives=2, husband_wives=None, subject_visit=self.bhs_subject_visit_male.id)
        form = DemographicsForm(data=self.data)
        self.assertTrue(form .is_valid())


