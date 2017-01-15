from django.test import TestCase, tag

from bcpp.surveys import BHS_SURVEY, AHS_SURVEY

from .test_mixins import SubjectMixin
from member.models.household_member import HouseholdMember
from member.clone import Clone
from bcpp_subject.models.appointment import Appointment
from bcpp_subject.models.subject_consent import SubjectConsent
from bcpp_subject.exceptions import ConsentValidationError
from member.models.enrollment_checklist import EnrollmentChecklist
from edc_constants.constants import NOT_APPLICABLE, YES
from datetime import timedelta
from dateutil.relativedelta import relativedelta


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

    def test_clone_carries_forward_enrollment_checklist_completed(self):
        household_structure = self.make_household_ready_for_enumeration()
        old_member = self.add_household_member(household_structure=household_structure)
        old_member = self.add_enrollment_checklist(old_member)
        old_member = self.add_subject_consent(old_member)

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)

        new_member = old_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)

        self.assertTrue(new_member.enrollment_checklist_completed)

    def test_clone_carries_forward_enrollment_checklist_notcompleted(self):
        household_structure = self.make_household_ready_for_enumeration()
        old_member = self.add_household_member(household_structure=household_structure)

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)

        new_member = old_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)

        self.assertFalse(new_member.enrollment_checklist_completed)

    def test_add_followup_subjectconsent_enrollment_checklist_completed(self):
        household_structure = self.make_household_ready_for_enumeration()
        old_member = self.add_household_member(household_structure=household_structure)
        old_member = self.add_enrollment_checklist(old_member)
        consent_data = {
            'identity': '31722515',
            'confirm_identity': '31722515',
            'report_datetime': self.get_utcnow(),
        }
        old_member = self.add_subject_consent(old_member, **consent_data)

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)
        self.assertTrue(old_member.eligible_member)
        new_member = old_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)
        new_member.save()

        new_member.inability_to_participate = NOT_APPLICABLE
        new_member.study_resident = YES
        new_member.save()

        new_member = HouseholdMember.objects.get(pk=new_member.pk)
        self.assertTrue(new_member.eligible_member)
        consent_data.update(report_datetime=self.get_utcnow() + relativedelta(years=1))
        new_member = self.add_subject_consent(new_member, **consent_data)
        self.assertEqual(SubjectConsent.objects.filter(subject_identifier=new_member.subject_identifier).count(), 2)

    def test_add_followup_subjectconsent_subject_identifier_same(self):
        household_structure = self.make_household_ready_for_enumeration()
        old_member = self.add_household_member(household_structure=household_structure)
        self.add_enrollment_checklist(old_member)
        self.add_subject_consent(old_member)

        old_member = HouseholdMember.objects.filter(
            household_structure=household_structure).first()

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)

        new_member = old_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)
        new_member.save()

        self.assertTrue(old_member.eligible_member)
        self.assertEqual(old_member.eligible_member, new_member.eligible_member)

        subject_consent = self.add_subject_consent(new_member)
        self.assertEqual(subject_consent.subject_identifier, new_member.subject_identifier)

    def test_add_a_followup_subject_consent(self):
        household_structure = self.make_household_ready_for_enumeration()
        old_member = self.add_household_member(household_structure=household_structure)
        self.add_enrollment_checklist(old_member)
        self.add_subject_consent(old_member)

        old_member = HouseholdMember.objects.filter(
            household_structure=household_structure).first()

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)

        new_member = old_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)
        self.assertEqual(old_member.subject_identifier, new_member.subject_identifier)

    def test_household_member_clone(self):
        household_structure = self.make_household_ready_for_enumeration()
        old_member = self.add_household_member(household_structure=household_structure)
        self.add_enrollment_checklist(old_member)
        self.add_subject_consent(old_member)

        old_member = HouseholdMember.objects.filter(
            household_structure=household_structure).first()

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)

        new_member = old_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)
        self.assertEqual(old_member.subject_identifier, new_member.subject_identifier)

        new_member.survey_schedule = next_household_structure.survey_schedule
        new_member.eligible_member = True
        new_member.study_resident = old_member.study_resident
        new_member.save_base()
#
#         new_obj = HouseholdMember.objects.get(pk=new_member.pk)
#         eligibility = self.add_enrollment_checklist(new_obj)

#
#         print(self.survey_schedule.next, "self.survey_schedule.next self.survey_schedule.next")
#
#         self.add_subject_consent(new_member)
        appt = Appointment.objects.all()
        print(appt)
#         print(SubjectConsent.objects.filter(subject_identifier=old_member.subject_identifier))
#         print(SubjectConsent.objects.filter(subject_identifier=new_member.subject_identifier))

#         self.assertEqual(old_member.internal_identifier, new_obj.internal_identifier)
#         self.assertEqual(new_obj.subject_identifier, new_obj.subject_identifier)

    def test_subject_consent_ahs(self):

        self.survey_schedule = self.get_survey_schedule(0)
        household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=self.survey_schedule)
        household_member_year1 = self.add_household_member(household_structure)
        print(household_member_year1.internal_identifier)
        self.add_subject_consent(household_member_year1)

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)

        Clone(household_structure=next_household_structure,
              report_datetime=self.get_utcnow()).clone(create=True)

#         new_household_member = HouseholdMember.objects.filter(
#             internal_identifier=household_member_year1.internal_identifier)

#         for new_member in clone.clone(create=True):
#             if new_member.first_name == household_member_year1.first_name and new_member.initials == household_member_year1.initials:
#                 print(new_member.internal_identifier)
#                 self.add_subject_consent(new_member)
#                 break

        #self.assertEqual(household_member_year2.subject_identifier, household_member_year1.subject_identifier)



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
