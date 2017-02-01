from django.test import TestCase, tag

from member.models.household_member import HouseholdMember
from survey.site_surveys import site_surveys

from ..models import EnrollmentBhs, EnrollmentAhs, EnrollmentEss, Enrollment
from .test_mixins import SubjectMixin


class TestEnrollment(SubjectMixin, TestCase):

    def test_first_survey(self):
        """Asserts for first survey member enrolled to BHS, if year-1.
        """
        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-1')
        household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)
        self.assertEqual(EnrollmentBhs.objects.all().count(), 1)

    @tag('EE')
    def test_second_survey(self):
        """Asserts for second survey member enrolled to AHS.
        """
        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-1')
        household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        household_member = self.add_household_member(
            household_structure=household_structure)
        household_member = self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(household_member)

        self.assertEqual(
            Enrollment.objects.filter(
                subject_identifier=subject_consent.subject_identifier).count(),
            1)

        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)
        household_member = household_member.clone(
            household_structure=household_structure,
            report_datetime=household_structure.survey_schedule_object.start)
        household_member = self.update_household_member_clone(household_member)
        print(3, household_member.subject_identifier)
        household_member = self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(household_member)
        print(4, household_member.subject_identifier)
        print(5, subject_consent.household_member.subject_identifier)
        print(6, subject_consent.subject_identifier)

        self.assertEqual(
            Enrollment.objects.filter(
                subject_identifier=subject_consent.subject_identifier).count(),
            2)

        self.assertEqual(EnrollmentBhs.objects.all().count(), 1)
        self.assertEqual(EnrollmentAhs.objects.all().count(), 1)

    def test_third_survey(self):
        """Asserts for third survey member enrolled to AHS.
        """
        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-1')
        household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)

        # second survey
        household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)
        household_member = household_member.clone(
            household_structure=household_structure,
            report_datetime=household_structure.enumerated_datetime)
        household_member = self.update_household_member_clone(household_member)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)

        # third survey
        household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)
        household_member = household_member.clone(
            household_structure=household_structure,
            report_datetime=household_structure.enumerated_datetime)
        household_member = self.update_household_member_clone(household_member)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)

        self.assertEqual(EnrollmentAhs.objects.all().count(), 2)
        self.assertEqual(EnrollmentBhs.objects.all().count(), 1)

    def test_first_survey_year2(self):
        """Asserts for first survey in year-2 member enrolled to BHS.
        """
        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-2')
        household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)
        self.assertEqual(EnrollmentBhs.objects.all().count(), 1)

    def test_second_survey_year3(self):
        """Asserts for second survey in year-3 member enrolled to AHS.
        """
        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-2')
        household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)

        household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)
        household_member = household_member.clone(
            household_structure=household_structure,
            report_datetime=household_structure.enumerated_datetime)
        household_member = self.update_household_member_clone(household_member)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)
        self.assertEqual(EnrollmentAhs.objects.all().count(), 1)

    def test_ess(self):
        """Asserts for first survey in year 3 member enrolled to ESS.
        """
        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-3')
        household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)

        self.assertEqual(EnrollmentEss.objects.all().count(), 1)
        self.assertEqual(EnrollmentAhs.objects.all().count(), 0)
        self.assertEqual(EnrollmentBhs.objects.all().count(), 0)
