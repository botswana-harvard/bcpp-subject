from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_registration.models import RegisteredSubject
from member.models.household_member.household_member import HouseholdMember
from survey.site_surveys import site_surveys

from ..models import SubjectConsent
from .test_mixins import SubjectMixin


class TestHouseholdMember(SubjectMixin, TestCase):

    def test_household_member_finds_consent(self):
        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-1')
        household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(household_member)
        self.assertEqual(
            subject_consent,
            household_member.consent)

    def test_household_member_knows_subject_identifier(self):
        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-1')
        household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(household_member)
        self.assertEqual(
            subject_consent.subject_identifier,
            household_member.subject_identifier)

    @tag('HH')
    def test_household_member_internal_identifier_in_registered_subject(self):
        """Asserts subject_consent creates RegisteredSubject.
        """
        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-1')
        household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(household_member)

        self.assertEqual(
            RegisteredSubject.objects.get(
                registration_identifier=household_member.internal_identifier
            ).subject_identifier,
            subject_consent.subject_identifier)

        self.assertEqual(
            RegisteredSubject.objects.get(
                registration_identifier=household_member.internal_identifier
            ).subject_identifier,
            household_member.subject_identifier)

    def test_household_member_finds_consent2(self):
        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-1')
        household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(
            household_member=household_member,
            report_datetime=household_structure.survey_schedule_object.start)
        self.assertEqual(
            subject_consent.version, '1')
        self.assertEqual(
            subject_consent,
            household_member.consent)

        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)
        household_member = household_member.clone(
            household_structure=household_structure,
            report_datetime=household_structure.survey_schedule_object.start)
        household_member = self.update_household_member_clone(household_member)
        household_member = self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(
            household_member=household_member,
            report_datetime=household_structure.survey_schedule_object.start)
        subject_consent = self.add_subject_consent(
            household_member=household_member,
            report_datetime=household_structure.survey_schedule_object.start)
        self.assertEqual(
            subject_consent.version, '2')
        self.assertEqual(
            subject_consent,
            household_member.consent)

    @tag('HH')
    def test_household_member_finds_consent3(self):
        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-1')
        household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(
            household_member=household_member,
            report_datetime=household_structure.survey_schedule_object.start)
        self.assertEqual(
            subject_consent.version, '1')
        self.assertEqual(
            subject_consent,
            household_member.consent)

        household_member = HouseholdMember.objects.get(pk=household_member.pk)
        household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)
        household_member = household_member.clone(
            household_structure=household_structure,
            report_datetime=household_structure.survey_schedule_object.start)
        household_member = self.update_household_member_clone(household_member)
        household_member = self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(
            household_member=household_member,
            report_datetime=household_structure.survey_schedule_object.start)
        self.assertEqual(
            subject_consent.version, '2')
        self.assertEqual(
            subject_consent,
            household_member.consent)

        for months in range(1, 72):
            new_consent = self.add_subject_consent(
                household_member=household_member,
                report_datetime=subject_consent.consent_datetime + relativedelta(months=months))
            if subject_consent != new_consent:
                subject_consent = new_consent
                break

        self.assertEqual(
            subject_consent.version, '3')

        for months in range(1, 72):
            new_consent = self.add_subject_consent(
                household_member=household_member,
                report_datetime=subject_consent.consent_datetime + relativedelta(months=months))
            if subject_consent != new_consent:
                subject_consent = new_consent
                break

        self.assertEqual(
            subject_consent.version, '4')

        for months in range(1, 72):
            new_consent = self.add_subject_consent(
                household_member=household_member,
                report_datetime=subject_consent.consent_datetime + relativedelta(months=months))
            if subject_consent != new_consent:
                subject_consent = new_consent
                break

        self.assertEqual(
            subject_consent.version, '5')

        survey_schedule_object = site_surveys.get_survey_schedule(
            'bcpp-survey.bcpp-year-3')
        household_structure = self.make_household_ready_for_enumeration(
            report_datetime=survey_schedule_object.start,
            survey_schedule=survey_schedule_object)
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)

        SubjectConsent.objects.get(
            version='5',
            subject_identifier=household_member.subject_identifier)

        self.assertEqual(
            subject_consent,
            household_member.consent)
