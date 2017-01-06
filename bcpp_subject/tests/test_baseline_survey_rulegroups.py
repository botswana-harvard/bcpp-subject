from model_mommy import mommy

from django.test import TestCase

from edc_constants.constants import NO, YES, POS, NEG
from edc_metadata.constants import REQUIRED, NOT_REQUIRED, KEYED
from edc_metadata.models import CrfMetadata

from member.models.household_member import HouseholdMember

from .test_mixins import SubjectMixin
from datetime import timedelta


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
