from django.test import TestCase, tag
from django.core.exceptions import ObjectDoesNotExist

from member.models.household_member import HouseholdMember
from survey.site_surveys import site_surveys

from ..models import EnrollmentBhs, EnrollmentAhs, EnrollmentEss

from .test_mixins import SubjectMixin


class TestSurveyAndConsent(SubjectMixin, TestCase):

    """Test survey, consent and enrollment sequence.
    Assert that the correct enrollment model is auto-
    completed."""

    survey_schedule_names = [
        'bcpp-survey.bcpp-year-1.test_community',
        'bcpp-survey.bcpp-year-2.test_community',
        'bcpp-survey.bcpp-year-3.test_community']

    def setUp(self):
        super().setUp()
        household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=self.survey_schedule_object[0],
            report_datetime=self.survey_schedule_object[0].start,
            make_hoh=False)
        self.household_member = self.add_household_member(
            household_structure,
            report_datetime=household_structure.report_datetime)
        self.assertTrue(self.household_member.eligible_member)
        self.assertFalse(self.household_member.eligible_subject)

    def clone(self, household_member):
        household_structure = self.get_next_household_structure_ready(
            household_member.household_structure,
            make_hoh=None)
        household_member.clone(household_structure)

    def test_subject_consent_attrs(self):
        subject_consent = self.add_subject_consent(
            self.household_member,
            report_datetime=self.household_member.report_datetime)
        self.assertEqual(
            subject_consent.consent_datetime,
            self.household_member.report_datetime)

        self.assertIsNotNone(subject_consent.survey_schedule)
        self.assertIsNotNone(subject_consent.survey_schedule_object)
        self.assertEqual(
            subject_consent.survey_schedule,
            self.survey_schedule_names[0])

    def test_subject_consent_chooses_enrollment_bhs(self):
        """Asserts enrolled to BHS in year 1.
        """
        subject_consent = self.add_subject_consent(
            self.household_member,
            report_datetime=self.household_member.report_datetime)

        try:
            enrollment = EnrollmentBhs.objects.get(
                subject_identifier=subject_consent.subject_identifier)
        except ObjectDoesNotExist:
            self.fail('EnrollmentBhs unexpectedly does not exist')

        self.assertEqual(
            enrollment.survey,
            'bcpp-survey.bcpp-year-1.bhs.test_community')

    def test_subject_consent_chooses_enrollment_ahs(self):
        """Asserts enrolled to AHS in year 2 if already enrolled in
        BHS year1.
        """
        subject_consent = self.add_subject_consent(
            self.household_member,
            report_datetime=self.household_member.report_datetime)

        household_member = self.clone(self.household_member)

        self.add_subject_consent(
            household_member,
            report_datetime=household_member.report_datetime)
        try:
            enrollment = EnrollmentAhs.objects.get(
                subject_identifier=subject_consent.subject_identifier)
        except ObjectDoesNotExist:
            self.fail('EnrollmentAhs unexpectedly does not exist')

        self.assertEqual(
            enrollment.survey,
            'bcpp-survey.bcpp-year-1.ahs.test_community')

    def test_subject_consent_chooses_enrollment_bhs2(self):
        """Asserts enrolled to BHS in year 2 if not enrolled in
        BHS year1.
        """
        household_member = self.household_members[1]
        subject_consent = self.add_subject_consent(
            household_member,
            report_datetime=household_member.report_datetime)

        try:
            enrollment = EnrollmentBhs.objects.get(
                subject_identifier=subject_consent.subject_identifier)
        except ObjectDoesNotExist:
            self.fail('EnrollmentBhs unexpectedly does not exist')

        self.assertEqual(
            enrollment.survey,
            'bcpp-survey.bcpp-year-2.bhs.test_community')

    def test_subject_consent_chooses_enrollment_ess(self):
        """Asserts enrolled to ESS in year 3 if not enrolled in
        anything previously.
        """
        household_member = self.household_members[2]
        subject_consent = self.add_subject_consent(
            household_member,
            report_datetime=household_member.report_datetime)

        try:
            enrollment = EnrollmentEss.objects.get(
                subject_identifier=subject_consent.subject_identifier)
        except ObjectDoesNotExist:
            self.fail('EnrollmentEss unexpectedly does not exist')

        self.assertEqual(
            enrollment.survey,
            'bcpp-survey.bcpp-year-3.ess.test_community')

    def test_subject_consent_chooses_enrollment_ahs1(self):
        """Asserts enrolled to AHS in year 3 if enrolled previously.
        """
        household_member = self.household_members[1]
        self.add_subject_consent(
            household_member,
            report_datetime=household_member.report_datetime)
        household_member = self.household_members[2]
        subject_consent = self.add_subject_consent(
            household_member,
            report_datetime=household_member.report_datetime)

        try:
            enrollment = EnrollmentAhs.objects.get(
                subject_identifier=subject_consent.subject_identifier)
        except ObjectDoesNotExist:
            self.fail('EnrollmentEss unexpectedly does not exist')

        self.assertEqual(
            enrollment.survey,
            'bcpp-survey.bcpp-year-3.ahs.test_community')

    def test_subject_consent_chooses_enrollment_ahs2(self):
        """Asserts enrolled to AHS in year 3 if enrolled previously.
        """
        household_member = self.household_members[0]
        self.add_subject_consent(
            household_member,
            report_datetime=household_member.report_datetime)
        household_member = self.household_members[2]
        subject_consent = self.add_subject_consent(
            household_member,
            report_datetime=household_member.report_datetime)

        try:
            enrollment = EnrollmentAhs.objects.get(
                subject_identifier=subject_consent.subject_identifier)
        except ObjectDoesNotExist:
            self.fail('EnrollmentEss unexpectedly does not exist')

        self.assertEqual(
            enrollment.survey,
            'bcpp-survey.bcpp-year-3.ahs.test_community')
