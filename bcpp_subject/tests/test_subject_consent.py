from datetime import timedelta
from dateutil.relativedelta import relativedelta
from faker import Faker

from django.core.exceptions import MultipleObjectsReturned
from django.test import TestCase, tag

from edc_base.utils import age
from edc_consent.consent import Consent
from edc_consent.site_consents import site_consents
from edc_constants.constants import NO, CONSENTED, FEMALE, MALE
from edc_metadata.models import CrfMetadata

from member.models import HouseholdMember

from ..constants import T0
from ..exceptions import ConsentValidationError
from ..models import Appointment
from .test_mixins import SubjectMixin


fake = Faker()


@tag('CC')
class TestSubjects(SubjectMixin, TestCase):

    def setUp(self):
        site_consents.backup_registry()
        self.consent_factory(
            start=self.study_open_datetime,
            end=self.study_open_datetime + timedelta(days=50),
            version='1.0')

    def consent_factory(self, **kwargs):
        options = dict(
            start=kwargs.get('start'),
            end=kwargs.get('end'),
            gender=kwargs.get('gender', [MALE, FEMALE]),
            updates_versions=kwargs.get('updates_versions', []),
            version=kwargs.get('version', '1'),
            age_min=kwargs.get('age_min', 16),
            age_max=kwargs.get('age_max', 64),
            age_is_adult=kwargs.get('age_is_adult', 18),
        )
        model = kwargs.get('model', 'bcpp_subject.subjectconsent')
        consent = Consent(model, **options)
        site_consents.register(consent)
        return consent

    def test_datetime(self):
        self.assertIsNotNone(self.get_utcnow())

    # subject consent
    def test_consent_updates_member_status(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.assertTrue(
            household_member.eligible_member)
        self.add_enrollment_checklist(household_member)
        self.assertTruel(household_member.eligible_subject)
        try:
            self.add_subject_consent(household_member=household_member)
        except ConsentValidationError:
            self.fail('ConsentValidationError unexpectedly raised')
        self.assertEqual(household_member.member_status, CONSENTED)

    def test_consent_updates_member(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(household_member)
        household_member = HouseholdMember.objects.get(
            pk=subject_consent.household_member.pk)
        self.assertTrue(household_member.is_consented)

    def test_consent_knows_study_site(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(household_member)
        self.assertTrue(subject_consent.study_site, '00')

    def test_consent_validates_with_enrollment_checklist_dob(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        enrollment_checklist = self.add_enrollment_checklist(household_member)
        self.assertRaises(
            ConsentValidationError,
            self.add_subject_consent,
            household_member=household_member,
            dob=enrollment_checklist.dob + relativedelta(days=1))

    def test_consent_validates_with_minor_dob(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        enrollment_checklist = self.add_enrollment_checklist(household_member)
        age_in_years = age(
            enrollment_checklist.dob, enrollment_checklist.report_datetime).years
        test_dob = enrollment_checklist.dob - \
            relativedelta(years=(age_in_years - 17))
        self.assertRaises(
            ConsentValidationError,
            self.add_subject_consent,
            household_member=household_member,
            consent_datetime=enrollment_checklist.report_datetime,
            dob=test_dob)

    def test_consent_validates_with_enrollment_checklist_literacy(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.assertRaises(
            ConsentValidationError,
            self.add_subject_consent,
            household_member=household_member,
            is_literate=NO, witness_name=fake.last_name())

    def test_consent_validates_with_enrollment_checklist_citizen(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.assertRaises(
            ConsentValidationError,
            self.add_subject_consent,
            household_member=household_member,
            citizen=NO)

    def test_consent_validates_with_enrollment_checklist_minor(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.assertRaises(
            ConsentValidationError,
            self.add_subject_consent,
            household_member=household_member,
            guardian_name=fake.name())

    def test_consent_updates_household_member_subject_identifier(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(
            household_member=household_member)
        household_member = HouseholdMember.objects.get(
            pk=subject_consent.household_member.pk)
        self.assertEqual(
            subject_consent.subject_identifier, household_member.subject_identifier)

    def test_consent_creates_appointment(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.assertRaises(
            Appointment.DoesNotExist,
            Appointment.objects.get,
            subject_identifier=household_member.subject_identifier)
        self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(
            household_member=household_member)
        household_member = HouseholdMember.objects.get(
            pk=subject_consent.household_member.pk)
        try:
            Appointment.objects.get(
                subject_identifier=household_member.subject_identifier)
        except Appointment.DoesNotExist:
            self.fail('Appointment.DoesNotExist unexpectedly raised.')
        except MultipleObjectsReturned:
            pass

    def test_visit_creates_all_appointments(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(
            household_member=household_member)
        household_member = HouseholdMember.objects.get(
            pk=subject_consent.household_member.pk)
        visit_codes = [appt.visit_code for appt in Appointment.objects.filter(
            subject_identifier=household_member.subject_identifier)]
        visit_codes.sort()
        self.assertEqual(['T0', 'T1', 'T2', 'T3'], visit_codes)

    def test_subject_visit_creates_metadata(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        subject_consent = self.add_subject_consent(
            household_member=household_member)
        subject_visit = self.add_subject_visits(
            visit_codes=[T0],
            subject_identifier=subject_consent.subject_identifier)
        self.assertGreater(
            CrfMetadata.objects.filter(
                subject_identifier=subject_visit.household_member.subject_identifier,
                visit_code='T0').count(), 0)
