from faker import Faker
from model_mommy import mommy

from edc_base_test.mixins import LoadListDataMixin

from member.list_data import list_data
from member.tests.test_mixins import MemberMixin
from member.constants import ELIGIBLE_FOR_CONSENT, HEAD_OF_HOUSEHOLD, ELIGIBLE_FOR_SCREENING
from member.models.enrollment_checklist import EnrollmentChecklist
from edc_constants.constants import NO, YES
from member.models.household_member.household_member import HouseholdMember


fake = Faker()


class SubjectTestMixin(MemberMixin, LoadListDataMixin):

    list_data = list_data


class SubjectMixin(SubjectTestMixin):

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
