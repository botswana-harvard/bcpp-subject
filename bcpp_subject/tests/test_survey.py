from django.test import TestCase, tag

from bcpp.surveys import BHS_SURVEY, AHS_SURVEY

from .test_mixins import SubjectMixin


@tag('erik')
class TestSurvey(SubjectMixin, TestCase):

    """Tests to assert survey attrs."""

    def test_subject_consent_attrs(self):
        self.survey_schedule = self.get_survey_schedule(0)

        household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=self.survey_schedule)

        household_member = self.add_household_member(
            household_structure)
        self.assertTrue(household_member.eligible_member)
        self.assertFalse(household_member.eligible_subject)

        subject_consent = self.make_subject_consent(household_member)

        self.assertIsNotNone(subject_consent.survey)
        self.assertIsNotNone(subject_consent.survey_object)
        self.assertIsNotNone(subject_consent.survey_schedule)
        self.assertIsNotNone(subject_consent.survey_schedule_object)

    def test_subject_consent_attr_values(self):
        self.survey_schedule = self.get_survey_schedule(0)

        household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=self.survey_schedule)

        household_member = self.add_household_member(
            household_structure)
        self.assertTrue(household_member.eligible_member)
        self.assertFalse(household_member.eligible_subject)

        subject_consent = self.make_subject_consent(household_member)

        self.assertEqual(
            subject_consent.survey,
            'bcpp-survey.bcpp-year-1.bhs.test_community')
        self.assertIsNotNone(
            subject_consent.survey_schedule,
            'bcpp-survey.bcpp-year-1.test_community')

    def test_subject_consent_chooses_survey(self):
        self.survey_schedule = self.get_survey_schedule(0)

        household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=self.survey_schedule)

        household_member = self.add_household_member(household_structure)

        subject_consent = self.make_subject_consent(household_member)

        self.assertEqual(subject_consent.survey_object.name, BHS_SURVEY)

    def test_subject_consent_chooses_survey2(self):

        self.survey_schedule = self.get_survey_schedule(0)
        household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=self.survey_schedule)
        household_member = self.add_household_member(household_structure)
        self.make_subject_consent(household_member)

        self.survey_schedule = self.survey_schedule.next
        household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=self.survey_schedule)
        household_member = self.add_household_member(household_structure)

        subject_consent = self.make_subject_consent(household_member)

        self.assertEqual(subject_consent.survey_object.name, AHS_SURVEY)


#     def test_subject_consent_survey_schedule_set_correctly(self):
# 
#         survey_schedules = site_surveys.get_survey_schedules(group_name='example-survey')
# 
#         if not survey_schedules:
#             raise AssertionError('survey_schedules is unexpectedly None')
# 
#         for index, survey_schedule in enumerate(
#                 site_surveys.get_survey_schedules(group_name='example-survey')):
#             household_structure = self.make_household_ready_for_enumeration(
#                 survey_schedule=survey_schedule)
#             household_member = self.add_household_member(household_structure)
#             self.assertEqual(
#                 household_member.survey_schedule,
#                 'example-survey.example-survey-{}.test_community'.format(index + 1))
#             self.assertEqual(
#                 household_member.survey_schedule_object.field_value,
#                 'example-survey.example-survey-{}.test_community'.format(index + 1))
#             self.assertEqual(
#                 household_member.survey_schedule_object.name,
#                 'example-survey-{}'.format(index + 1))
#             self.assertEqual(
#                 household_member.survey_schedule_object.group_name,
#                 'example-survey')
#             self.assertEqual(
#                 household_member.survey_schedule_object.short_name,
#                 'example-survey.example-survey-{}'.format(index + 1))
