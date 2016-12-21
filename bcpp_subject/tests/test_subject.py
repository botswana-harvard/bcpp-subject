from dateutil.relativedelta import relativedelta
from faker import Faker

from django.test import TestCase, tag

from edc_constants.constants import NO, CONSENTED

from member.constants import ELIGIBLE_FOR_CONSENT, ELIGIBLE_FOR_SCREENING
from member.models import HouseholdMember

from ..exceptions import ConsentValidationError

from .test_mixins import SubjectMixin


fake = Faker()


class TestSubjects(SubjectMixin, TestCase):

    def test_datetime(self):
        self.assertIsNotNone(self.get_utcnow())

    # subject consent
    def test_consent_updates_member_status(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(household_structure=household_structure)
        self.assertEqual(household_member.member_status, ELIGIBLE_FOR_SCREENING)
        self.add_enrollment_checklist(household_member)
        self.assertEqual(household_member.member_status, ELIGIBLE_FOR_CONSENT)
        try:
            self.make_subject_consent(household_member=household_member)
        except ConsentValidationError:
            self.fail('ConsentValidationError unexpectedly raised')
        self.assertEqual(household_member.member_status, CONSENTED)

    def test_consent_updates_member(self):
        subject_consent = self.make_subject_consent()
        household_member = HouseholdMember.objects.get(pk=subject_consent.household_member.pk)
        self.assertTrue(household_member.is_consented)

    def test_consent_knows_study_site(self):
        subject_consent = self.make_subject_consent()
        self.assertTrue(subject_consent.study_site, '00')

    def test_consent_validates_with_enrollment_checklist_dob(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(household_structure=household_structure)
        enrollment_checklist = self.add_enrollment_checklist(household_member)
        self.assertRaises(
            ConsentValidationError,
            self.make_subject_consent,
            household_member=household_member,
            dob=enrollment_checklist.dob + relativedelta(days=1))

    @tag('me')
    def test_consent_validates_with_enrollment_checklist_literacy(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(household_structure=household_structure)
        self.assertRaises(
            ConsentValidationError,
            self.make_subject_consent,
            household_member=household_member,
            is_literate=NO, witness_name=fake.last_name())

    def test_consent_validates_with_enrollment_checklist_citizen(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(household_structure=household_structure)
        self.assertRaises(
            ConsentValidationError,
            self.make_subject_consent,
            household_member=household_member,
            citizen=NO)

    def test_consent_validates_with_enrollment_checklist_minor(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(household_structure=household_structure)
        self.assertRaises(
            ConsentValidationError,
            self.make_subject_consent,
            household_member=household_member,
            guardian_name=fake.name())
