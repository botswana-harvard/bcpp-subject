from django.test import TestCase

from edc_constants.constants import NO, YES

from ..forms import ReproductiveHealthForm

from .test_mixins import SubjectMixin

from bcpp_subject.models.list_models import FamilyPlanning


class TestReproductiveHealthForm(SubjectMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.family_planning = FamilyPlanning.objects.create(
            name='Condoms, consistent use (male or female)', 
            short_name='Condoms, consistent use (male or female)')
        self.options = {
            'number_children': 4,
            'menopause': NO,
            'family_planning': [str(self.family_planning.id)],
            'family_planning_other': None,
            'currently_pregnant': YES,
            'when_pregnant': YES,
            'gestational_weeks': 2,
            'pregnancy_hiv_tested': NO,
            'pregnancy_hiv_retested': YES,
            'subject_visit': self.subject_visit_female.id,
            'report_datetime': self.get_utcnow(),
        }

    def test_valid_form(self):
        form = ReproductiveHealthForm(data=self.options)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())

    def test_if_participant_is_not_pregnant_since_last_interview(self):
        """Asserts that participant is not pregnant."""
        self.options.update(when_pregnant=NO, gestational_weeks=2)
        form = ReproductiveHealthForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_participant_has_reached_menopause(self):
        """Asserts that participant has reached menopause."""
        planning = FamilyPlanning.objects.create(
            name='Injectable contraceptive',
            short_name='Injectable contraceptive')
        self.options.update(menopause=YES, family_planning=[str(planning.id)])
        form = ReproductiveHealthForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_menopause_then_no_pregnancy(self):
        """Asserts that participant reached menopause then she cannot be pregnant."""
        self.options.update(menopause=YES, currently_pregnant=YES)
        form = ReproductiveHealthForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_no_menopause_then_provide_family_planning_details(self):
        """Asserts that participant has not reached menopause then family 
        planning details should be provided."""
        self.options.update(menopause=NO, family_planning=None)
        form = ReproductiveHealthForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_no_menopause_pregagnancy_status(self):
        """Asserts that participant has not reached menopause, is she currently pregnant?"""
        self.options.update(menopause=NO, currently_pregnant=None)
        form = ReproductiveHealthForm(data=self.options)
        self.assertFalse(form.is_valid())
