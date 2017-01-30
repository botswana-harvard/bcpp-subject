from dateutil.relativedelta import relativedelta

from django.core.exceptions import MultipleObjectsReturned
from django.test import TestCase, tag

from edc_registration.models import RegisteredSubject
from member.models.household_member.household_member import HouseholdMember
from survey.site_surveys import site_surveys

from .test_mixins import SubjectMixin
from bcpp_subject.models.subject_consent import SubjectConsent
from edc_registration.exceptions import RegisteredSubjectError


class TestRegisteredSubject(SubjectMixin, TestCase):

    def setUp(self):
        """Consents member into the first survey.
        """
        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-1')
        self.household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        self.household_member = self.add_household_member(
            household_structure=self.household_structure)
        self.add_enrollment_checklist(self.household_member)
        self.subject_consent = self.add_subject_consent(self.household_member)

    def create_next_household_and_consent(self, household_member,
                                          household_structure,
                                          **consent_options):
        """Creates next household_structure, clones the member
        and adds a consent.
        """
        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)
        household_member = household_member.clone(
            household_structure=household_structure,
            report_datetime=household_structure.survey_schedule_object.start)
        household_member = self.update_household_member_clone(household_member)
        household_member = self.add_enrollment_checklist(household_member)
        return self.add_subject_consent(
            household_member=household_member,
            report_datetime=household_structure.survey_schedule_object.start,
            **consent_options)

    def test_consent_creates_registered_subject(self):
        """Asserts registered subject carries values from
        the subject consent.
        """

        registered_subject = RegisteredSubject.objects.get(
            registration_identifier=self.household_member.internal_identifier)

        self.assertIsNotNone(registered_subject.subject_identifier)
        self.assertEqual(
            registered_subject.subject_identifier,
            self.subject_consent.subject_identifier)

        self.assertIsNotNone(registered_subject.identity)
        self.assertEqual(
            registered_subject.identity,
            self.subject_consent.identity)

        self.assertIsNotNone(registered_subject.first_name)
        self.assertEqual(
            registered_subject.first_name,
            self.subject_consent.first_name)

        self.assertIsNotNone(registered_subject.dob)
        self.assertEqual(
            registered_subject.dob,
            self.subject_consent.dob)

        self.assertIsNotNone(registered_subject.initials)
        self.assertEqual(
            registered_subject.initials,
            self.subject_consent.initials)

        self.assertIsNotNone(registered_subject.last_name)
        self.assertEqual(
            registered_subject.last_name,
            self.subject_consent.last_name)

        self.assertIsNotNone(registered_subject.gender)
        self.assertEqual(
            registered_subject.gender,
            self.subject_consent.gender)

    def test_consent_creates_one_registered_subject(self):
        """Asserts only one RegisteredSubject instance is ever
        created for a consented member.
        """
        # consent into second survey
        subject_consent = self.create_next_household_and_consent(
            self.household_member, self.household_structure)
        household_member = subject_consent.household_member

        # create more consents for this subject
        for _ in ['3', '4', '5']:
            for months in range(1, 72):
                new_consent = self.add_subject_consent(
                    household_member=household_member,
                    report_datetime=(subject_consent.consent_datetime
                                     + relativedelta(months=months)))
                if subject_consent != new_consent:
                    subject_consent = new_consent
                    break
        # confirm multiple consents for same member
        self.assertEqual(
            5, SubjectConsent.objects.filter(
                subject_identifier=household_member.subject_identifier).count())
        # verify single instance
        try:
            RegisteredSubject.objects.get(
                registration_identifier=household_member.internal_identifier)
        except MultipleObjectsReturned:
            self.fail('MultipleObjectsReturned unexpectedly raised')
        try:
            RegisteredSubject.objects.get(
                subject_identifier=subject_consent.subject_identifier)
        except MultipleObjectsReturned:
            self.fail('MultipleObjectsReturned unexpectedly raised')
        try:
            RegisteredSubject.objects.get(
                identity=subject_consent.identity)
        except MultipleObjectsReturned:
            self.fail('MultipleObjectsReturned unexpectedly raised')

    def test_conflict_raises_error(self):
        """Asserts an exception is raised if a key value, such as
        identity, is changed in follow-up consents for the same
        household member.
        """
        try:
            self.create_next_household_and_consent(
                self.household_member,
                self.household_structure,
                identity='1212121212',
                confirm_identity='1212121212')
        except RegisteredSubjectError:
            pass
        else:
            self.fail('RegisteredSubjectError not raised')
