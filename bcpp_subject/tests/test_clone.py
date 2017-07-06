from dateutil.relativedelta import relativedelta

from django.test import TestCase, tag

from edc_constants.constants import YES

from member_clone.clone import Clone
from member.constants import ABLE_TO_PARTICIPATE
from member.models import HouseholdMember

from ..constants import T1, T2
from .test_mixins import SubjectMixin


class TestClone(SubjectMixin, TestCase):

    def test_clone_carries_forward_enrollment_checklist_completed(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)

        new_member = household_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)

        self.assertTrue(new_member.enrollment_checklist_completed)

    def test_clone_carries_forward_enrollment_checklist_notcompleted(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = self.add_household_member(
            household_structure=household_structure)

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)

        new_member = household_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)

        self.assertFalse(new_member.enrollment_checklist_completed)

    def test_add_followup_subjectconsent_enrollment_checklist_completed(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        consent_data = {
            'identity': '31722515',
            'confirm_identity': '31722515',
            'report_datetime': self.get_utcnow(),
        }
        subject_consent = self.add_subject_consent(
            household_member, **consent_data)

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)
        self.assertTrue(subject_consent.household_member.eligible_member)
        new_member = subject_consent.household_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)
        new_member.save()

        new_member.inability_to_participate = ABLE_TO_PARTICIPATE
        new_member.study_resident = YES
        new_member.save()

        new_member = HouseholdMember.objects.get(pk=new_member.pk)
        self.assertTrue(new_member.eligible_member)
        consent_data.update(
            report_datetime=self.get_utcnow() + relativedelta(years=1))
        subject_consent = self.add_subject_consent(new_member, **consent_data)

    def test_add_followup_subjectconsent_subject_identifier_same(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)
        household_member = HouseholdMember.objects.get(pk=household_member.pk)

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)

        new_member = household_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)
        new_member.save()

        self.assertTrue(household_member.eligible_member)
        self.assertEqual(
            household_member.eligible_member, new_member.eligible_member)

        subject_consent = self.add_subject_consent(new_member)
        self.assertEqual(
            subject_consent.subject_identifier, new_member.subject_identifier)

    def test_add_a_followup_subject_consent(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)
        household_member = HouseholdMember.objects.get(pk=household_member.pk)

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)

        new_member = household_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)
        self.assertEqual(
            household_member.subject_identifier, new_member.subject_identifier)

    def test_household_member_clone(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)

        household_member = HouseholdMember.objects.get(pk=household_member.pk)

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)

        new_member = household_member.clone(
            household_structure=next_household_structure,
            report_datetime=next_household_structure.enumerated_datetime)
        self.assertEqual(
            household_member.subject_identifier, new_member.subject_identifier)

        new_member.survey_schedule = next_household_structure.survey_schedule
        new_member.eligible_member = True
        new_member.study_resident = household_member.study_resident
        new_member.save_base()

    def test_add_visitfollowup(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)

        report_datetime = self.get_utcnow() + relativedelta(years=1)
        t1_visit = self.add_subject_visit_followup(
            household_member, T1, report_datetime)
        self.assertEqual(t1_visit.visit_code, T1)

    def test_add_visitfollowup_T2(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = self.add_household_member(
            household_structure=household_structure)
        self.add_enrollment_checklist(household_member)
        self.add_subject_consent(household_member)

        report_datetime = self.get_utcnow() + relativedelta(years=1)
        t1_visit = self.add_subject_visit_followup(
            household_member, T1, report_datetime)
        self.assertEqual(t1_visit.visit_code, T1)
        report_datetime = self.get_utcnow() + relativedelta(years=2)
        t2_visit = self.add_subject_visit_followup(
            t1_visit.household_member, T2, report_datetime)
        self.assertEqual(t2_visit.visit_code, T2)

    def test_subject_consent_ahs(self):

        self.survey_schedule = self.get_survey_schedule(0)
        household_structure = self.make_household_ready_for_enumeration(
            survey_schedule=self.survey_schedule)
        household_member_year1 = self.add_household_member(household_structure)
        self.add_subject_consent(household_member_year1)

        next_household_structure = self.get_next_household_structure_ready(
            household_structure, make_hoh=None)

        Clone(household_structure=next_household_structure,
              report_datetime=self.get_utcnow()).clone(create=True)
