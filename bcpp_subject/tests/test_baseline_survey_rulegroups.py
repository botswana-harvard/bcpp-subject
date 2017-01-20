from model_mommy import mommy

from datetime import timedelta
from django.test import TestCase

from edc_constants.constants import NO, YES, POS, NEG, IND, UNK
from edc_metadata.constants import REQUIRED, NOT_REQUIRED, KEYED

from member.models.household_member import HouseholdMember

from ..constants import NOT_SURE, T0, VIRAL_LOAD, RESEARCH_BLOOD_DRAW

from .rule_group_mixins import RuleGroupMixin


class TestBaselineRuleSurveyRuleGroups(RuleGroupMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.consent_data_female = {
            'identity': '31722515',
            'confirm_identity': '31722515',
            'report_datetime': self.get_utcnow(),
        }
        self.consent_data_male = {
            'identity': '31721515',
            'confirm_identity': '31721515',
            'report_datetime': self.get_utcnow(),
        }
        self.subject_visit_male = self.make_subject_visit_for_consented_subject_male('T0', **self.consent_data_male)
        self.subject_visit_female = self.make_subject_visit_for_consented_subject_female('T0', **self.consent_data_female)
        self.household_member = HouseholdMember.objects.filter(
            subject_identifier=self.subject_visit_male.subject_identifier)
        self.subject_identifier = self.subject_visit_male.subject_identifier
        self.hiv_test_date = self.get_utcnow() - timedelta(days=50)

    def test_hiv_car_adherence_and_pima1(self):
        """ HIV Positive took arv in the past but now defaulting, Should NOT offer POC CD4.

        Models:
            * HivCareAdherence
            * HivResult
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED, T0, self.subject_identifier).count(), 1)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, NO, YES, NO, NO)

        # said they have taken ARV so not required
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_hiv_car_adherence_and_pima2(self):
        """If POS and on arv and have doc evidence, Pima not required, not a defaulter.

        Models:
            * HivCareAdherence
            * HivResult
        """
        self.subject_identifier = self.subject_visit_female.subject_identifier
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED, T0, self.subject_identifier).count(), 1)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.subject_visit_female, self.get_utcnow(), NO, NO, NO, YES, YES)

        # on art so no need for CD4
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_hiv_car_adherence_and_pima3(self):
        """If POS and on arv but do not have doc evidence, Pima required.

        Models:
            * HivCareAdherence
            * HivResult
        """

        self.subject_identifier = self.subject_visit_male.subject_identifier
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED, T0, self.subject_identifier).count(), 1)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, NO, NO, YES, NO)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_newly_pos_and_not_art_bhs(self):
        """Newly HIV Positive not on ART at T0, Should offer POC CD4.
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        self.make_hiv_result(POS, self.subject_visit_male, self.get_utcnow())

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, NO, NO, NO, NO)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_not_known_pos_runs_hiv_and_cd4(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""
        self.subject_identifier = self.subject_visit_male.subject_identifier
        # add hivtestreview,
        hiv_test_review = self.make_hivtest_review(self.subject_visit_male, NEG, self.get_utcnow(), self.hiv_test_date)

        def assert_crfs():
            self.assertEqual(
                self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED, T0, self.subject_identifier).count(), 1)
            self.assertEqual(
                self.crf_metadata_obj('bcpp_subject.hivresult', REQUIRED, T0, self.subject_identifier).count(), 1)
            self.assertEqual(
                self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)
        assert_crfs()

        hiv_test_review.recorded_hiv_result = IND
        hiv_test_review.save()
        assert_crfs()

        hiv_test_review.recorded_hiv_result = UNK
        hiv_test_review.save()
        assert_crfs()

    def test_known_pos_completes_hiv_care_adherence(self):
        """If known POS (not including today's test), requires hiv_care_adherence."""
        self.subject_identifier = self.subject_visit_male.subject_identifier

        # add hivtestreview
        self.make_hivtest_review(self.subject_visit_male, POS, self.get_utcnow(), self.hiv_test_date)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_known_neg_does_not_complete_hiv_care_adherence(self):
        """If known POS (not including today's test), requires hiv_care_adherence."""
        self.subject_identifier = self.subject_visit_male.subject_identifier
        # add HivTestHistory,
        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, YES, POS, NO)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtestinghistory', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtestreview', REQUIRED, T0, self.subject_identifier).count(), 1)

        # add HivTestReview,
        self.make_hivtest_review(self.subject_visit_male, NEG, self.get_utcnow(), self.hiv_test_date)

        # hiv_care_adherence.save()

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj(
                'bcpp_subject.hivcareadherence', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_known_neg_requires_hiv_test_today(self):
        """If previous result is NEG, need to test today (HivResult).

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier
        # add HivTestReview
        self.make_hivtest_review(self.subject_visit_male, NEG, self.get_utcnow(), self.hiv_test_date)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivresult', REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_known_pos_does_not_require_hiv_test_today(self):
        """If previous result is POS, do not need to test today (HivResult).

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        # add hivtestreview
        self.make_hivtest_review(self.subject_visit_male, POS, self.get_utcnow(), self.hiv_test_date)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_known_pos_stigma_forms(self):
        """If known posetive, test stigma forms
        """
        self.subject_identifier = self.subject_visit_female.subject_identifier
        #  self.check_male_registered_subject_rule_groups(self.subject_visit_female_T0)
        self.make_hivtesting_history(self.subject_visit_female, self.get_utcnow(), YES, YES, NEG, NO)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtestinghistory', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.stigma', REQUIRED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.stigmaopinion', REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_hiv_tested_forms(self):
        """If known posetive, test hivtested forms
        """
        self.subject_identifier = self.subject_visit_female.subject_identifier
        #  self.check_male_registered_subject_rule_groups(self.subject_visit_female_T0

        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            report_datetime=self.get_utcnow(),
            subject_visit=self.subject_visit_female,
        )
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtestinghistory', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtested', REQUIRED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivuntested', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

#         hiv_testing_history.has_tested = NO
#         hiv_testing_history.save()

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivuntested', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtested', REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_known_pos_on_art_no_doc_requires_cd4_only(self):
        """If previous result is POS on art but no evidence, need to run CD4 (Pima).

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        # add HivTestReview,
        self.make_hivtest_review(self.subject_visit_male, POS, self.get_utcnow(), self.hiv_test_date)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED, T0, self.subject_identifier).count(), 1)

        # add HivCareAdherence,
        hivcareadherence = self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, NO, NO, YES, NO)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivcareadherence', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

        hivcareadherence.on_arv = NO
        hivcareadherence.save()
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_hiv_care_adherance_for_verbal_posetive_only(self):
        """HivCareAdharance form should be made available any verbal positive,
            not considering availability or lack thereof documentation.
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, NO)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_known_pos_on_art_with_doc_requires_cd4_only(self):
        """If previous result is POS on art with doc evidence, do not run HIV or CD4.

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier
        # add HivTestReview,
        self.make_hivtest_review(self.subject_visit_male, POS, self.get_utcnow(), self.hiv_test_date)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED, T0, self.subject_identifier).count(), 1)

        # add HivCareAdherence,
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, NO, NO, YES, YES)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivcareadherence', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_known_pos_no_art_but_has_doc_requires_cd4_only(self):
        """If previous result is POS on art but no evidence, need to run CD4 (Pima).

        This is a defaulter

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        # add HivTestReview,
        self.make_hivtest_review(self.subject_visit_male, POS, self.get_utcnow(), self.hiv_test_date)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED, T0, self.subject_identifier).count(), 1)

        # add HivCareAdherence,
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, NO, NO, NO, YES)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivcareadherence', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

    def test_elisaresult_behaves_like_todayhivresult(self):
        """when an elisa result is keyed in, a +ve result should result in RBD and VL
            being REQUIRED just like Today's HivResult
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        # add HivTestReview,
        self.make_hivtest_review(self.subject_visit_male, NEG, self.get_utcnow(), self.hiv_test_date)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivresult', REQUIRED, T0, self.subject_identifier).count(), 1)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.elisahivresult', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

        self.make_hiv_result(IND, self.subject_visit_male, self.get_utcnow())

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.elisahivresult', REQUIRED, T0, self.subject_identifier).count(), 1)

        self.make_requisition(self.subject_visit_male, 'ELISA', self.get_utcnow())

        mommy.make_recipe(
            'bcpp_subject.elisahivresult', subject_visit=self.subject_visit_male, report_datetime=self.get_utcnow(),
            hiv_result=POS,
            hiv_result_datetime=self.get_utcnow()
        )
        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.elisahivresult', KEYED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(self.requisition_metadata_obj(REQUIRED, T0, VIRAL_LOAD, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj(REQUIRED, T0, RESEARCH_BLOOD_DRAW, self.subject_identifier).count(), 1)

    def test_normal_circumsition_in_y1(self):
        self.subject_identifier = self.subject_visit_male.subject_identifier

        def assert_circumsition(circumsition_entry_status, uncircumcised_entry_status, circumcised_entry_status):
            self.assertEqual(
                self.crf_metadata_obj(
                    'bcpp_subject.circumcision', circumsition_entry_status, T0, self.subject_identifier).count(), 1)
            self.assertEqual(
                self.crf_metadata_obj(
                    'bcpp_subject.uncircumcised', uncircumcised_entry_status, T0, self.subject_identifier).count(), 1)
            self.assertEqual(
                self.crf_metadata_obj(
                    'bcpp_subject.circumcised', circumcised_entry_status, T0, self.subject_identifier).count(), 1)
        assert_circumsition(REQUIRED, REQUIRED, REQUIRED)

        circumcition = mommy.make_recipe(
            'bcpp_subject.circumcision', subject_visit=self.subject_visit_male, report_datetime=self.get_utcnow(),
            circumcised=YES
        )
        assert_circumsition(KEYED, NOT_REQUIRED, REQUIRED)

        self.make_hiv_result(NEG, self.subject_visit_male, self.get_utcnow())

        # Enforce that entering an HivResult does not affect Circumcition Meta Data.
        assert_circumsition(KEYED, NOT_REQUIRED, REQUIRED)

        circumcition.circumcised = NO
        circumcition.save()
        # uncircumcised is required,
        assert_circumsition(KEYED, REQUIRED, NOT_REQUIRED)

        circumcition.circumcised = NOT_SURE
        circumcition.save()

        assert_circumsition(KEYED, NOT_REQUIRED, NOT_REQUIRED)

    def test_Known_hiv_pos_y1_require_no_testing(self):
        self.subject_identifier = self.subject_visit_male.subject_identifier

        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, YES, POS, NO)

        self.make_hivtest_review(self.subject_visit_male, POS, self.get_utcnow(), self.hiv_test_date)

        self.assertEqual(
            self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

    def hiv_pos_nd_art_naive_at_bhs(self):
        """Enrollees at t0 who are HIV-positive and ART naive at BHS.
           Pima, RBD and VL required. Then Key RBD for later use in Annual survey.
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier
        # Known POS in T0

        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, YES, POS, NO)

        self.make_hivtest_review(self.subject_visit_male, POS, self.get_utcnow(), self.hiv_test_date)

        self.assertEqual(self.requisition_metadata_obj(
            'bcpp_subject.subjectrequisition', REQUIRED, T0, RESEARCH_BLOOD_DRAW, self.subject_identifier).count(), 1)

        self.make_requisition(self.subject_visit_male, RESEARCH_BLOOD_DRAW, self.get_utcnow())

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, NO, NO, NO, NO)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(self.requisition_metadata_obj(REQUIRED, T0, VIRAL_LOAD, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj(KEYED, T0, RESEARCH_BLOOD_DRAW, self.subject_identifier).count(), 1)

    def test_hiv_pos_nd_not_on_art_at_bhs(self):
        """HIV Positive not on ART at T0, Should offer POC CD4, RBD and VL.
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier
        # Known POS in T0
        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, YES, POS, NO)

        self.make_hivtest_review(self.subject_visit_male, POS, self.get_utcnow(), self.hiv_test_date)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.subject_visit_male, self.get_utcnow(), NO, NO, NO, NO, NO)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T0, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj(REQUIRED, T0, VIRAL_LOAD, self.subject_identifier).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj(REQUIRED, T0, RESEARCH_BLOOD_DRAW, self.subject_identifier).count(), 1)

    def test_partner_forms_know_pos(self):
        """HIV Positive not on ART at T0, Should offer POC CD4, RBD and VL.
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier
        # make
        self.make_hivtesting_history(self.subject_visit_male, self.get_utcnow(), YES, NO, POS, NO)
        # Known POS in T0
        mommy.make_recipe(
            'bcpp_subject.sexualbehaviour',
            ever_sex=YES,
            lifetime_sex_partners=1,
            last_year_partners=1
        )

        self.assertEqual(
            self.crf_metadata_obj(
                'bcpp_subject.recentpartner', REQUIRED, T0, self.subject_identifier).count(), 1)

        self.assertEqual(
            self.crf_metadata_obj(
                'bcpp_subject.secondpartner', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

        self.assertEqual(
            self.crf_metadata_obj(
                'bcpp_subject.thirdpartner', NOT_REQUIRED, T0, self.subject_identifier).count(), 1)

