from model_mommy import mommy

from django.test import TestCase, tag

from .test_mixins import SubjectMixin
from member.constants import ELIGIBLE_FOR_CONSENT


class TestMembers(SubjectMixin, TestCase):

    def test_create_subjectconsent(self):
        household_structure = self.make_household_ready_for_enumeration()
        household_member = self.add_household_member(household_structure)
        self.add_enrollment_checklist(household_member)
        self.assertEqual(household_member.member_status, ELIGIBLE_FOR_CONSENT)
        mommy.make_recipe('bcpp_subject.subjectconsent')
