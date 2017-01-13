from django.test import TestCase, tag

from edc_base_test.exceptions import TestMixinError
from household.models.household_structure.household_structure import HouseholdStructure

from .test_mixins import SubjectMixin
from edc_constants.constants import MALE
from dateutil.relativedelta import relativedelta
from survey.site_surveys import site_surveys


class TestMixinsTests(SubjectMixin, TestCase):

    def setUp(self):
        self.household_structure = self.make_household_ready_for_enumeration(make_hoh=False)

    def test_make_consent_no_member(self):
        obj = self.add_subject_consent()
        self.assertIsNotNone(obj)

    def test_make_consent(self):
        household_structure = HouseholdStructure.objects.all()[0]
        household_member = self.add_household_member(household_structure)
        self.add_subject_consent(household_member)

    def test_make_consent_incorrectly(self):
        household_structure = HouseholdStructure.objects.all()[0]
        household_member = self.add_household_member(household_structure)
        self.assertRaises(
            TestMixinError,
            self.add_subject_consent, household_member, household_structure.survey_schedule)

    def test_make_consent_with_options(self):
        household_structure = HouseholdStructure.objects.all()[0]
        household_member = self.add_household_member(
            household_structure, age_in_years=32, gender=MALE)
        obj = self.add_subject_consent(household_member)
        self.assertEqual(obj.gender, MALE)
        self.assertEqual(obj.dob, (self.get_utcnow() - relativedelta(years=32)).date())


@tag('erik1')
class TestConsentSurvey(SubjectMixin, TestCase):

    def test_make_consent_first_survey(self):
        first_household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=site_surveys.get_survey_schedules()[0],
            make_hoh=False)
        first_household_member = self.add_household_member(
            household_structure=first_household_structure)
        obj = self.add_subject_consent(first_household_member)
        self.assertEqual(
            obj.survey_schedule_object.field_value,
            'bcpp-survey.bcpp-year-1.test_community')
        self.assertEqual(
            obj.survey_object.field_value,
            'bcpp-survey.bcpp-year-1.bhs.test_community')

    def test_make_consent_next_survey(self):
        first_household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=site_surveys.get_survey_schedules()[0],
            make_hoh=False)
        first_household_member = self.add_household_member(
            household_structure=first_household_structure)
        self.add_subject_consent(first_household_member)

        household_structure = self.make_household_ready_for_next(
            household_structure=first_household_structure, make_hoh=False)
        household_member = self.add_household_member(household_structure)
        obj = self.add_subject_consent(household_member)
        self.assertEqual(
            obj.survey_schedule_object.field_value,
            'bcpp-survey.bcpp-year-2.test_community')
        self.assertEqual(
            obj.survey_object.field_value,
            'bcpp-survey.bcpp-year-2.ahs.test_community')

    @tag('aa')
    def test_make_consent_next_next_survey(self):
        first_household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=site_surveys.get_survey_schedules()[0],
            make_hoh=False)
        first_household_member = self.add_household_member(
            household_structure=first_household_structure)

        self.add_subject_consent(first_household_member)
        household_structure = self.make_household_ready_for_next(
            household_structure=first_household_structure, make_hoh=False)
        household_member = self.add_household_member(household_structure)
        self.add_subject_consent(household_member)

        household_structure = self.make_household_ready_for_next(
            household_structure, make_hoh=False)
        household_member = self.add_household_member(household_structure)
        obj = self.add_subject_consent(household_member)

        self.assertEqual(
            obj.survey_schedule_object.field_value,
            'bcpp-survey.bcpp-year-3.test_community')
        self.assertEqual(
            obj.survey_object.field_value,
            'bcpp-survey.bcpp-year-3.ahs.test_community')

    def test_make_consent_ess_survey(self):

        household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=site_surveys.get_survey_schedules()[-1],
            make_hoh=False)

        household_member = self.add_household_member(household_structure)
        obj = self.add_subject_consent(household_member)
        self.assertEqual(
            obj.survey_schedule_object.field_value,
            'bcpp-survey.bcpp-year-3.test_community')
        self.assertEqual(
            obj.survey_object.field_value,
            'bcpp-survey.bcpp-year-3.ess.test_community')
