from model_mommy import mommy

from django.test import TestCase

from edc_constants.constants import NO, YES, POS, NEG
from edc_metadata.constants import REQUIRED, NOT_REQUIRED, KEYED
from edc_metadata.models import CrfMetadata, RequisitionMetadata

from member.models.household_member import HouseholdMember

from .test_mixins import SubjectMixin
from datetime import timedelta
from bcpp_subject.labs import elisa_panel, viral_load_panel, rdb_panel
from bcpp_subject.constants import NOT_SURE


class TestBaselineRuleSurveyRuleGroups(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit_male = self.make_subject_visit_for_a_male_subject('T0')
        self.subject_visit_female = self.make_subject_visit_for_consented_subject('T0')
        self.household_member = HouseholdMember.objects.filter(
            subject_identifier=self.subject_visit_male.subject_identifier)
        self.subject_identifier = self.subject_visit_male.subject_identifier

    def crf_metadata_obj(self, model, entry_status):
        return CrfMetadata.objects.filter(
            entry_status=entry_status,
            model=model,
            subject_identifier=self.subject_identifier)

    def requisition_metadata_obj(self, model, entry_status, panel_name):
        return RequisitionMetadata.objects.filter(
            entry_status=entry_status,
            model=model,
            subject_identifier=self.subject_identifier,
            panel_name=panel_name)

    def test_hiv_car_adherence_and_pima1(self):
        """ HIV Positive took arv in the past but now defaulting, Should NOT offer POC CD4.

        Models:
            * HivCareAdherence
            * HivResult
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED).count(), 1)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)

        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=YES,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )
        # said they have taken ARV so not required
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, ).count(), 1)

    def test_hiv_car_adherence_and_pima2(self):
        """If POS and on arv and have doc evidence, Pima not required, not a defaulter.

        Models:
            * HivCareAdherence
            * HivResult
        """
        self.subject_identifier = self.subject_visit_female.subject_identifier

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED).count(), 1)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)

        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            report_datetime=self.get_utcnow(),
            subject_visit=self.subject_visit_female,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=YES,
            arv_evidence=YES,
        )
        # on art so no need for CD4
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)

    def test_hiv_car_adherence_and_pima3(self):
        """If POS and on arv but do not have doc evidence, Pima required.

        Models:
            * HivCareAdherence
            * HivResult
        """

        self.subject_identifier = self.subject_visit_male.subject_identifier

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED).count(), 1)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)

        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            report_datetime=self.get_utcnow(),
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=YES,
            arv_evidence=NO,
        )
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)

    def hiv_result(self, status, subject_visit):
        """ Create HivResult for a particular survey"""
        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=subject_visit, report_datetime=self.get_utcnow(),
            panel_name='Microtube',
        )
        hiv_result = mommy.make_recipe(
            'bcpp_subject.hivresult', subject_visit=subject_visit, report_datetime=self.get_utcnow(),
            hiv_result=status, insufficient_vol=NO
        )
        return hiv_result

    def test_newly_pos_and_not_art_bhs(self):
        """Newly HIV Positive not on ART at T0, Should offer POC CD4.
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        self.hiv_result(POS, self.subject_visit_male)

        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            report_datetime=self.get_utcnow(),
            subject_visit=self.subject_visit_male,
            first_positive=None,
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,
        )

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED).count(), 1)

    def hivtest_review(self, hiv_status):
        hiv_test_review = mommy.make_recipe(
            'bcpp_subject.hivtestreview',
            report_datetime=self.get_utcnow(),
            subject_visit=self.subject_visit_male,
            hiv_test_date=self.get_utcnow() - timedelta(days=50),
            recorded_hiv_result=hiv_status)
        return hiv_test_review

    def test_not_known_pos_runs_hiv_and_cd4(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""
        self.subject_identifier = self.subject_visit_male.subject_identifier
        # add hivtestreview,
        hiv_test_review = self.hivtest_review(NEG)

        def assert_crfs():
            self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED).count(), 1)
            self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', REQUIRED).count(), 1)
            self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)
        assert_crfs()

        hiv_test_review.recorded_hiv_result = 'IND'
        hiv_test_review.save()
        assert_crfs()

        hiv_test_review.recorded_hiv_result = 'UNK'
        hiv_test_review.save()
        assert_crfs()

    def test_known_pos_completes_hiv_care_adherence(self):
        """If known POS (not including today's test), requires hiv_care_adherence."""
        self.subject_identifier = self.subject_visit_male.subject_identifier

        # add hivtestreview
        self.hivtest_review(POS)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED).count(), 1)

    def test_known_neg_does_not_complete_hiv_care_adherence(self):
        """If known POS (not including today's test), requires hiv_care_adherence."""
        self.subject_identifier = self.subject_visit_male.subject_identifier
        # add HivTestHistory,
        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            report_datetime=self.get_utcnow(),
            subject_visit=self.subject_visit_male,
        )
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestinghistory', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestreview', REQUIRED).count(), 1)

        # add HivTestReview,
        self.hivtest_review(NEG)
        # hiv_care_adherence.save()

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED).count(), 1)

    def test_known_neg_requires_hiv_test_today(self):
        """If previous result is NEG, need to test today (HivResult).

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier
        # add HivTestReview
        self.hivtest_review(NEG)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', REQUIRED).count(), 1)

    def test_known_pos_does_not_require_hiv_test_today(self):
        """If previous result is POS, do not need to test today (HivResult).

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        # add hivtestreview
        self.hivtest_review(POS)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED).count(), 1)

    def test_known_pos_stigma_forms(self):
        """If known posetive, test stigma forms
        """
        self.subject_identifier = self.subject_visit_female.subject_identifier
        #  self.check_male_registered_subject_rule_groups(self.subject_visit_female_T0)

        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            report_datetime=self.get_utcnow(),
            subject_visit=self.subject_visit_female,
        )

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestinghistory', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.stigma', REQUIRED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.stigmaopinion', REQUIRED).count(), 1)

    def test_hiv_tested_forms(self):
        """If known posetive, test hivtested forms
        """
        self.subject_identifier = self.subject_visit_female.subject_identifier
        #  self.check_male_registered_subject_rule_groups(self.subject_visit_female_T0

        hiv_testing_history = mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            report_datetime=self.get_utcnow(),
            subject_visit=self.subject_visit_female,
        )
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestinghistory', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtested', REQUIRED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivuntested', NOT_REQUIRED).count(), 1)

        hiv_testing_history.has_tested = NO
        hiv_testing_history.save()

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivuntested', NOT_REQUIRED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtested', REQUIRED).count(), 1)

    def test_known_pos_on_art_no_doc_requires_cd4_only(self):
        """If previous result is POS on art but no evidence, need to run CD4 (Pima).

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        # add HivTestReview,
        self.hivtest_review(POS)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED).count(), 1)

        # add HivCareAdherence,
        hivcareadherence = mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=YES,
            arv_evidence=NO,
        )
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)

        hivcareadherence.on_arv = NO
        hivcareadherence.save()
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED).count(), 1)

    def test_hiv_care_adherance_for_verbal_posetive_only(self):
        """HivCareAdharance form should be made available any verbal positive,
            not considering availability or lack thereof documentation.
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            report_datetime=self.get_utcnow(),
            subject_visit=self.subject_visit_male,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=NO,
            other_record=NO)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED).count(), 1)

    def test_known_pos_on_art_with_doc_requires_cd4_only(self):
        """If previous result is POS on art with doc evidence, do not run HIV or CD4.

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier
        # add HivTestReview,
        self.hivtest_review(POS)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED).count(), 1)

        # add HivCareAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)

    def test_known_pos_no_art_but_has_doc_requires_cd4_only(self):
        """If previous result is POS on art but no evidence, need to run CD4 (Pima).

        This is a defaulter

        See rule_groups.ReviewNotPositiveRuleGroup and
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        # add HivTestReview,
        self.hivtest_review(POS)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', KEYED).count(), 1)

        # add HivCareAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=YES,  # this is the rule field
        )
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestreview', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', KEYED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED).count(), 1)

    def test_elisaresult_behaves_like_todayhivresult(self):
        """when an elisa result is keyed in, a +ve result should result in RBD and VL
            being REQUIRED just like Today's HivResult
        """
        self.subject_identifier = self.subject_visit_male.subject_identifier

        # add HivTestReview,
        self.hivtest_review(NEG)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', REQUIRED).count(), 1)

        self.hiv_result('IND', self.subject_visit_male)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.elisahivresult', REQUIRED).count(), 1)

        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.subject_visit_male, report_datetime=self.get_utcnow(),
            panel_name=elisa_panel, hiv_result=POS, hiv_result_datetime=self.get_utcnow()
        )

        mommy.make_recipe(
            'bcpp_subject.elisahivresult', subject_visit=self.subject_visit_male, report_datetime=self.get_utcnow(),
            panel_name=elisa_panel,
        )
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.elisahivresult', KEYED).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, viral_load_panel).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, rdb_panel).count(), 1)

    def test_normal_circumsition_in_y1(self):

        self.subject_identifier = self.subject_visit_male.subject_identifier

        def assert_circumsition(circumsition_entry_status, uncircumcised_entry_status, circumcised_entry_status):
            self.assertEqual(self.crf_metadata_obj('bcpp_subject.circumsition', circumsition_entry_status).count(), 1)
            self.assertEqual(self.crf_metadata_obj('bcpp_subject.uncircumcised', uncircumcised_entry_status).count(), 1)
            self.assertEqual(self.crf_metadata_obj('bcpp_subject.circumcised', circumcised_entry_status).count(), 1)
        assert_circumsition(REQUIRED, REQUIRED, REQUIRED)

        circumcition = mommy.make_recipe(
            'bcpp_subject.circumcision', subject_visit=self.subject_visit_male, report_datetime=self.get_utcnow(),
            circumcised=YES
        )
        assert_circumsition(KEYED, NOT_REQUIRED, REQUIRED)

        self.hiv_result(NEG, self.subject_visit_male)

        # Enforce that entering an HivResult does not affect Circumcition Meta Data.
        assert_circumsition(KEYED, NOT_REQUIRED, REQUIRED)

        circumcition.circumcised = NO
        circumcition.save()

        assert_circumsition(KEYED, REQUIRED, NOT_REQUIRED)

        circumcition.circumcised = NOT_SURE
        circumcition.save()

        assert_circumsition(KEYED, NOT_REQUIRED, NOT_REQUIRED)

