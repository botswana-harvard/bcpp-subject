from datetime import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker
from model_mommy import mommy

from edc_base_test.exceptions import TestMixinError
from edc_base_test.mixins import AddVisitMixin, CompleteCrfsMixin
from edc_base_test.mixins import LoadListDataMixin
from edc_constants.constants import NO, YES, NOT_APPLICABLE, MALE
from edc_metadata.models import CrfMetadata
from member.constants import ELIGIBLE_FOR_CONSENT, HEAD_OF_HOUSEHOLD, ELIGIBLE_FOR_SCREENING
from member.list_data import list_data
from member.models.enrollment_checklist import EnrollmentChecklist
from member.models.household_member.household_member import HouseholdMember
from member.tests.mixins import MemberMixin

from ..constants import T0
from ..models import Appointment

fake = Faker()


class SubjectTestMixin(MemberMixin, LoadListDataMixin):

    list_data = list_data


class SubjectMixin(SubjectTestMixin, AddVisitMixin):

    bcpp_subject_model_label = 'bcpp_subject.subjectvisit'

    def setUp(self):
        super(SubjectMixin, self).setUp()
        self.study_site = '40'

    def add_subject_consent(self, household_member=None, survey_schedule=None, **options):
        """Returns a subject consent in an enumerated household.

            * Consents the given `household_member`. If `household_member`=None
                will create one using `options` then consent him/her.
            * Adds the enrollment checklist for the `household_member`,
                if it does not exist.
            * Creates a HoH household member if one does not already already exist.
        """

        if household_member and survey_schedule:
            raise TestMixinError(
                'If \'household_member\' is specified, \'survey_schedule\' is not required.')
        if not household_member:
            survey_schedule = survey_schedule or self.get_survey_schedule(0)

        try:
            make_hoh = False if household_member.relation == HEAD_OF_HOUSEHOLD else True
        except AttributeError:
            make_hoh = True

        household_structure = self.make_household_ready_for_enumeration(
            make_hoh=make_hoh, survey_schedule=survey_schedule)

        # add an additional member if not provided
        if not household_member:
            household_member = self.add_household_member(
                household_structure, relation='cousin', **options)
            self.assertTrue(household_member.eligible_member)

        # add enrollment checklist for household_member, if it does not exist
        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(
                household_member__subject_identifier=household_member.subject_identifier)
            self.assertTrue(enrollment_checklist.is_eligible)
        except EnrollmentChecklist.DoesNotExist:
            self.assertEqual(
                household_member.member_status, ELIGIBLE_FOR_SCREENING)
            enrollment_checklist = self.add_enrollment_checklist(
                household_member, **options)
            household_member = HouseholdMember.objects.get(pk=household_member.pk)
            self.assertEqual(household_member.member_status, ELIGIBLE_FOR_CONSENT)

        # update options for subject consent from enrollment checklist
        consent_options = dict(
            consent_datetime=options.get('report_datetime') or self.get_utcnow(),
            dob=options.get('dob', enrollment_checklist.dob),
            gender=options.get('gender', enrollment_checklist.gender),
            initials=options.get('initials', enrollment_checklist.initials),
            is_literate=options.get(
                'is_literate', enrollment_checklist.literacy),
            witness_name=options.get(
                'witness_name',
                fake.last_name() if enrollment_checklist.literacy == NO else None),
            legal_marriage=options.get(
                'legal_marriage', enrollment_checklist.legal_marriage),
            marriage_certificate=options.get(
                'marriage_certificate', enrollment_checklist.marriage_certificate),
            guardian_name=options.get(
                'guardian_name',
                fake.name() if enrollment_checklist.guardian == YES else None),
            identity=options.get('identity'),
            confirm_identity=options.get('confirm_identity'))

        # add subject consent
        mommy.make_recipe(
            'bcpp_subject.subjectconsent',
            household_member=household_member,
            survey_schedule=household_member.household_structure.survey_schedule,
            **consent_options)

        return HouseholdMember.objects.get(pk=household_member.pk)

    def add_subject_visits(self, visit_codes, subject_identifier):
        return self.add_visits(
            *visit_codes,
            model_label=self.bcpp_subject_model_label,
            subject_identifier=subject_identifier)

    def make_subject_visit_for_consented_subject_female(
            self, visit_code, report_datetime=None, survey=None, **options):
        """Returns a subject visit the given visit_code.

        Creates all needed relations."""
        household_structure = self.make_household_ready_for_enumeration()
        old_member = self.add_household_member(household_structure=household_structure)
        old_member = self.add_enrollment_checklist(old_member)
        old_member = self.add_subject_consent(old_member, **options)
        household_member = HouseholdMember.objects.get(pk=old_member.pk)
        appointment = Appointment.objects.get(
            subject_identifier=household_member.subject_identifier,
            visit_code=visit_code)
        return mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=household_member,
            subject_identifier=household_member.subject_identifier,
            appointment=appointment,
            report_datetime=report_datetime or self.get_utcnow())

    def make_subject_visit_for_consented_subject_male(self, visit_code, report_datetime=None, **options):
        """Returns a subject visit of a consented male member."""
        household_structure = self.make_enumerated_household_with_male_member()
        old_member = self.add_household_member(household_structure=household_structure, gender=MALE)
        old_member = self.add_enrollment_checklist(old_member)
        old_member = self.add_subject_consent(old_member, **options)
        household_member = HouseholdMember.objects.get(pk=old_member.pk)
        appointment = Appointment.objects.get(
            subject_identifier=household_member.subject_identifier,
            visit_code=visit_code)
        return mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=household_member,
            subject_identifier=household_member.subject_identifier,
            appointment=appointment,
            report_datetime=report_datetime or self.get_utcnow())

    def make_subject_visit_ahs_subject(self, visit_code, survey=None, report_datetime=None):
        """Returns a subject visit of a consented male member."""
        bhs_subject_visit = self.make_subject_visit_for_a_male_subject(T0)
        bhs_household_member = bhs_subject_visit.household_member
        # Create an ahs member
        household_member = self.make_ahs_household_member(
            bhs_household_member, survey=survey)
        appointment = Appointment.objects.get(
            subject_identifier=household_member.subject_identifier,
            visit_code=visit_code)
        return mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=household_member,
            subject_identifier=household_member.subject_identifier,
            appointment=appointment,
            report_datetime=report_datetime or self.get_utcnow() + datetime.timedelta(3 * 365 / 12))

    def add_subject_visit_followup(self, previous_member, visit_code, report_datetime):

        next_household_structure = self.get_next_household_structure_ready(
            previous_member.household_structure, make_hoh=None)

        new_member = previous_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)
        new_member.save()

        new_member.inability_to_participate = NOT_APPLICABLE
        new_member.study_resident = YES
        new_member.save()

        new_member = HouseholdMember.objects.get(pk=new_member.pk)
        self.consent_data.update(report_datetime=report_datetime)
        new_member = self.add_subject_consent(new_member, **self.consent_data)
        appointment = Appointment.objects.get(
            subject_identifier=new_member.subject_identifier,
            visit_code=visit_code)
        return mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=new_member,
            subject_identifier=new_member.subject_identifier,
            appointment=appointment,
            report_datetime=report_datetime)


class CompleteCrfsMixin(CompleteCrfsMixin, SubjectMixin):

    def complete_required_subject_crfs(self, visit_codes, subject_identifier):
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
