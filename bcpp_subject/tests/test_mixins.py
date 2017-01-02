from faker import Faker
from model_mommy import mommy

from edc_base_test.mixins import LoadListDataMixin

from member.list_data import list_data
from member.tests.test_mixins import MemberMixin
from member.constants import ELIGIBLE_FOR_CONSENT, HEAD_OF_HOUSEHOLD, ELIGIBLE_FOR_SCREENING
from member.models.enrollment_checklist import EnrollmentChecklist
from edc_constants.constants import NO, YES
from member.models.household_member.household_member import HouseholdMember
from edc_appointment.models import Appointment
from edc_base_test.mixins import AddVisitMixin, CompleteCrfsMixin
from edc_metadata.models import CrfMetadata

fake = Faker()


class SubjectTestMixin(MemberMixin, LoadListDataMixin):

    list_data = list_data


class SubjectMixin(SubjectTestMixin, AddVisitMixin):

    bcpp_subject_model_label = 'bcpp_subject.subjectvisit'

    def setUp(self):
        super(SubjectMixin, self).setUp()
        self.study_site = '40'

    def make_subject_consent(self, household_member=None, **options):
        """Returns a subject consent in an enumerated household.

        * Creates a HoH household member if one does not already already exist.
        * Adds an additional household_member unless provided. (This is the household_member to be
          enrolled and consented).
        * Adds the enrollment checklist for the provided or the additional household_member.
        * Adds the subject_consent for the provided or the additional household_member.
        """
        # set up plot, household, household_structure
        # add HoH if he/she does not already exist
        try:
            make_hoh = False if household_member.relation == HEAD_OF_HOUSEHOLD else True
        except AttributeError:
            make_hoh = True
        household_structure = self.make_household_ready_for_enumeration(make_hoh=make_hoh)
        # add an additional member if not provided
        if not household_member:
            household_member = self.add_household_member(household_structure, relation='cousin')
        # add enrollment checklist, if it does not exist
        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(household_member=household_member)
            self.assertEqual(household_member.member_status, ELIGIBLE_FOR_CONSENT)
        except EnrollmentChecklist.DoesNotExist:
            self.assertEqual(household_member.member_status, ELIGIBLE_FOR_SCREENING)
            enrollment_checklist = self.add_enrollment_checklist(household_member)
            household_member = HouseholdMember.objects.get(pk=household_member.pk)
            self.assertEqual(household_member.member_status, ELIGIBLE_FOR_CONSENT)
        # update options for subject consent from enrollment checklist
        options.update(
            consent_datetime=options.get('consent_datetime', enrollment_checklist.report_datetime),
            dob=options.get('dob', enrollment_checklist.dob),
            gender=options.get('gender', enrollment_checklist.gender),
            initials=options.get('initials', enrollment_checklist.initials),
            is_literate=options.get('is_literate', enrollment_checklist.literacy),
            witness_name=options.get('witness_name', fake.last_name() if enrollment_checklist.literacy == NO else None),
            legal_marriage=options.get('legal_marriage', enrollment_checklist.legal_marriage),
            marriage_certificate=options.get('marriage_certificate', enrollment_checklist.marriage_certificate),
            guardian_name=options.get('guardian_name', fake.name() if enrollment_checklist.guardian == YES else None),
        )
        # add subject consent
        subject_consent = mommy.make_recipe(
            'bcpp_subject.subjectconsent',
            household_member=household_member,
            **options)
        return subject_consent

    def add_subject_visits(self, *visit_codes, subject_identifier):
        return self.add_visits(
            *visit_codes,
            model_label=self.bcpp_subject_model_label,
            subject_identifier=subject_identifier)

    def make_subject_visit_for_consented_subject(self, visit_code, report_datetime=None):
        """Returns a subject visit the given visit_code.

        Creates all needed relations."""
        household_structure = self.make_household_ready_for_enumeration()
        household_member = HouseholdMember.objects.get(household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        subject_consent = self.make_subject_consent(household_member=household_member)
        household_member = HouseholdMember.objects.get(pk=subject_consent.household_member.pk)
        appointment = Appointment.objects.get(
            subject_identifier=household_member.subject_identifier,
            visit_code=visit_code)
        return mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=household_member,
            appointment=appointment,
            report_datetime=report_datetime or self.get_utcnow())


class CompleteCrfsMixin(CompleteCrfsMixin, SubjectMixin):

    def complete_required_subject_crfs(self, *visit_codes, subject_identifier):
        """Complete all required CRFs for a visit(s) using mommy defaults."""
        complete_required_crfs = {}
        for visit_code in visit_codes:
            subject_visit = self.add_subject_visits(visit_code, subject_identifier)
            completed_crfs = super(CompleteCrfsMixin, self).complete_required_crfs(
                visit_code=visit_code,
                visit=subject_visit,
                visit_attr='subject_visit',
                subject_identifier=subject_identifier)
            complete_required_crfs.update({visit_code: completed_crfs})
        return complete_required_crfs

    def get_crfs(self, visit_code=None, subject_identifier=None):
        """Return a queryset of crf metadata for the visit."""
        return CrfMetadata.objects.filter(
            subject_identifier=subject_identifier,
            visit_code=visit_code).exclude(
                model__in=['bcpp_subject.hivresult', 'bcpp_subject.subjectreferral']).order_by('show_order')
