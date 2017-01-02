from model_mommy import mommy

from django.test import TestCase

from edc_base.utils import get_utcnow

from .test_mixins import SubjectMixin
from bcpp_subject.forms.demographics_form import DemographicsForm
from bcpp_subject.models.subject_consent import SubjectConsent
from edc_constants.constants import MALE


class TestDemographicsForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')
        self.ethnic_groups = mommy.make_recipe('bcpp_subject.ethnicgroups', )
        self.live_with = mommy.make_recipe(
            'bcpp_subject.livewith', name='Partner or spouse', short_name='Partner or spouse')
        self.religion = mommy.make_recipe('bcpp_subject.religion')
        self.options = {
            'ethnic_other': '',
            'husband_wives': 0,
            'marital_status': 'Married',
            'num_wives': 2,
            'live_with': [self.live_with.id],
            'religion': [self.religion.id],
            'religion_other': u'',
            'report_datetime': get_utcnow(),
            'subject_visit': self.subject_visit.id,
            'ethnic': [self.ethnic_groups.id]
        }
        demo_form = DemographicsForm(data=self.options)
        self.assertTrue(demo_form.is_valid())

    def test_marriage_gender_female(self):
        """ A female should specify number of husbands otherwise throw validation error"""
        self.options.update(num_wives=0, husband_wives=10)
        form = DemographicsForm(data=self.options)
        self.assertFalse(form.is_valid())

        self.options.update(num_wives=2, husband_wives=0)
        form = DemographicsForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_marriage_gender_male(self):
        """ A male should specify number of wives otherwise throw validation error"""
        subject_consent = SubjectConsent.objects.filter(
            subject_identifier=self.subject_visit.subject_identifier).last()
        subject_consent.gender = MALE
        subject_consent.save_base(update_fields=['gender'])

        self.options.update(num_wives=10, husband_wives=0)
        form = DemographicsForm(data=self.options)
        self.assertFalse(form.is_valid())

        self.options.update(num_wives=0, husband_wives=2)
        form = DemographicsForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_marriage_gender(self):
        """ A married partipant should specify number of husbands or number of wives, otherwise if not specify throw
            validation error
        """
        self.options.update(num_wives=0, husband_wives=0)
        form = DemographicsForm(data=self.options)
        self.assertFalse(form.is_valid())
