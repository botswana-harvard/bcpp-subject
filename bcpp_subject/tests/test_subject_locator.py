from django.test import TestCase

from edc_constants.constants import YES, NO, NOT_APPLICABLE

from .test_mixins import SubjectMixin
from ..forms import SubjectLocatorForm


class TestSubjectLocatorForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.consent_data = {
            'identity': '31721515',
            'confirm_identity': '31721515',
        }
        self.bhs_subject_visit_female = self.make_subject_visit_for_consented_subject_female('E0', **self.consent_data)
        self.options = {
            'date_signed': self.get_utcnow(),
            'home_visit_permission': YES,
            'may_sms_follow_up': NO,
            'physical_address': 'Blue house',
            'subject_cell': '72777777',
            'may_follow_up': YES,
            'may_call_work': NO,
            'may_contact_someone': NO,
            'has_alt_contact': NOT_APPLICABLE,
            'subject_identifier': self.bhs_subject_visit_female.subject_identifier,
            'report_datetime': self.get_utcnow(),
        }

    def test_locator_form_valid(self):
        """Assert form valid and can be filled after consent."""
        form = SubjectLocatorForm(data=self.options)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save)

    def test_add_locator_before_consent(self):
        """Assert form not valid if cosent not filled."""
        household_structure = self.make_household_ready_for_enumeration()
        old_member = self.add_household_member(household_structure=household_structure)
        old_member = self.add_enrollment_checklist(old_member)
        self.options.update(
            subject_identifier=old_member.subject_identifier)
        form = SubjectLocatorForm(data=self.options)
        self.assertFalse(form.is_valid())
