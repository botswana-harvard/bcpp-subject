from django.test import TestCase, tag

from .rule_group_mixins import RuleGroupMixin

from edc_constants.constants import NO, YES
from edc_metadata.constants import NOT_REQUIRED
from bcpp_subject.constants import E0


class TestSubjectRuleGroup(RuleGroupMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.consent_data = {
            'identity': '31721515',
            'confirm_identity': '31721515',
            'report_datetime': self.get_utcnow(),
        }
        self.subject_visit = self.make_subject_visit_for_consented_subject_male(
            'E0', **self.consent_data)

    @tag("ess_rules")
    def test_rule_ess_rules(self):
        # add HivCarAdherence,
        self.make_hiv_care_adherence(
            self.subject_visit, self.get_utcnow(), NO, NO, YES, NO, NO)

        self.assertEqual(
            self.crf_metadata_obj(
                'bcpp_subject.pima', NOT_REQUIRED, E0, self.subject_identifier).count(), 1)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(
            self.subject_visit_male, self.get_utcnow(), NO, NO, YES, NO, NO)

        # said they have taken ARV so not required
        self.assertEqual(self.crf_metadata_obj(
            'bcpp_subject.pima', NOT_REQUIRED, E0, self.subject_identifier).count(), 1)
