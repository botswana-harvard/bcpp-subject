import datetime
from datetime import timedelta

from model_mommy import mommy

from django.test import TestCase

from edc_constants.constants import NO, YES, POS, NEG
from edc_metadata.constants import REQUIRED, NOT_REQUIRED, KEYED
from edc_metadata.models import CrfMetadata, RequisitionMetadata
from survey.site_surveys import site_surveys

from .test_mixins import SubjectMixin
from ..constants import T0, T1, T2, MICROTUBE, VIRAL_LOAD, RESEARCH_BLOOD_DRAW
from ..models import Appointment

from unittest.case import skip


class TestAnnualRuleSurveyRuleGroups(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.visit_code_T1 = T1
        self.bhs_subject_visit_male = self.make_subject_visit_for_a_male_subject(T0)
        self.subject_identifier = self.bhs_subject_visit_male.subject_identifier
        self.ahs_subject_visit_male_y2 = None
        self.ahs_subject_visit_male_y3 = None

    def crf_metadata_obj(self, model, entry_status, visit_code):
        return CrfMetadata.objects.filter(
            entry_status=entry_status,
            model=model,
            visit_code=visit_code,
            subject_identifier=self.subject_identifier)

    def requisition_metadata_obj(self, model, entry_status, visit_code, panel_name):
        return RequisitionMetadata.objects.filter(
            entry_status=entry_status,
            model=model,
            subject_identifier=self.subject_identifier,
            panel_name=panel_name,
            visit_code=visit_code)

    def hivtest_review(self, subject_visit, hiv_status, report_datetime=None):
        report_datetime = report_datetime or self.get_utcnow()
        hiv_test_review = mommy.make_recipe(
            'bcpp_subject.hivtestreview',
            report_datetime=report_datetime,
            subject_visit=subject_visit,
            hiv_test_date=self.get_utcnow() - timedelta(days=50),
            recorded_hiv_result=hiv_status)
        return hiv_test_review

    def make_hivtesting_history(self, subject_visit, has_tested, has_record, verbal_hiv_result, other_record, report_datetime=None):
        report_datetime = report_datetime or self.get_utcnow()
        hivtesting_history = mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            subject_visit=subject_visit,
            report_datetime=report_datetime,
            has_tested=has_tested,
            when_hiv_test='1 to 5 months ago',
            has_record=has_record,
            verbal_hiv_result=verbal_hiv_result,
            other_record=other_record
        )
        return hivtesting_history

    def make_subject_locator(self, subject_identifier, report_datetime=None):
        report_datetime = report_datetime or self.get_utcnow()
        subject_locator = mommy.make_recipe(
            'bcpp_subject.subjectlocator',
            subject_identifier=self.subject_identifier,
            report_datetime=report_datetime)
        return subject_locator

    def make_residency_mobility(self, subject_visit, permanent_resident, intend_residency, report_datetime=None):
        report_datetime = report_datetime or self.get_utcnow()
        residency_mobility = mommy.make_recipe(
            'bcpp_subject.residencymobility',
            subject_visit=subject_visit,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12),
            permanent_resident=permanent_resident,
            intend_residency=permanent_resident)
        return residency_mobility

    def make_requisition(self, subject_visit, panel, report_datetime=None):
        report_datetime = report_datetime or self.get_utcnow()
        subject_requisition = mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=subject_visit, report_datetime=report_datetime,
            panel_name=panel,
        )
        return subject_requisition

    def hiv_result(self, status, subject_visit, report_datetime=None):
        """ Create HivResult for a particular survey"""
        report_datetime = report_datetime or self.get_utcnow()
        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=subject_visit, report_datetime=report_datetime,
            panel_name=MICROTUBE,
        )
        hiv_result = mommy.make_recipe(
            'bcpp_subject.hivresult', subject_visit=subject_visit, report_datetime=report_datetime,
            hiv_result=status, insufficient_vol=NO
        )
        return hiv_result

    def make_hic_enrolment(self, subject_visit, hic_permission, report_datetime=None):
        """Return an hic enrolment instance."""
        report_datetime = report_datetime or self.get_utcnow()
        return mommy.make_recipe(
            'bcpp_subject.hicenrollment',
            subject_visit=subject_visit,
            report_datetime=self.get_utcnow(),
            hic_permission=hic_permission)

    def make_hivcareadherence(self, subject_visit, report_datetime=None):
        report_datetime = report_datetime or self.get_utcnow()
        return mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            subject_visit=subject_visit,
            report_datetime=report_datetime,
            first_positive=None,
            medical_care=None,
            ever_recommended_arv=None,
            ever_taken_arv=NO,
            first_arv=None,
            on_arv=NO,
            clinic_receiving_from=None,
            next_appointment_date=None,
            arv_stop_date=None,
            arv_stop=None,
            adherence_4_day=None,
            adherence_4_wk=None,
            arv_evidence=NO)

    def make_hiv_care_adherence(
            self, subject_visit, ever_recommended_arv, medical_care, ever_taken_arv, on_arv, arv_evidence, report_datetime):
        hiv_care_adherence = mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=subject_visit,
            report_datetime=self.get_utcnow(),
            medical_care=medical_care,
            ever_recommended_arv=ever_recommended_arv,
            ever_taken_arv=ever_taken_arv,
            on_arv=on_arv,
            arv_evidence=arv_evidence,  # this is the rule field
        )
        return hiv_care_adherence

    def hiv_pos_nd_art_naive_at_bhs(self):
        """Enrollees at t0 who are HIV-positive and ART naive at BHS.
           Pima, RBD and VL required. Then Key RBD for later use in Annual survey.
        """

        # Known POS in T0
        self.make_hivtesting_history(self.bhs_subject_visit_male, YES, YES, POS, NO, self.bhs_subject_visit_male.report_datetime)

        self.hivtest_review(self.bhs_subject_visit_male, POS, self.bhs_subject_visit_male.report_datetime)

        self.assertEqual(
            self.requisition_metadata_obj(
                'bcpp_subject.subjectrequisition', REQUIRED, T0, RESEARCH_BLOOD_DRAW).count(), 1)

        self.make_requisition(self.bhs_subject_visit_male, RESEARCH_BLOOD_DRAW, self.bhs_subject_visit_male.report_datetime)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.bhs_subject_visit_male, NO, NO, NO, NO, NO, self.bhs_subject_visit_male.report_datetime)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T0).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T0, VIRAL_LOAD).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', KEYED, T0, RESEARCH_BLOOD_DRAW).count(), 1)

    def ahs_y2_subject_visit(self):
        """Return an ahs subject visit."""
        # Create an ahs member
        survey = site_surveys.current_surveys[1]
        household_member = super().make_ahs_household_member(self.bhs_subject_visit_male.household_member, survey)
        appointment = Appointment.objects.get(
            subject_identifier=household_member.subject_identifier,
            visit_code=self.visit_code_T1)

        return mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=household_member,
            subject_identifier=household_member.subject_identifier,
            appointment=appointment,
            report_datetime=self.get_utcnow() + datetime.timedelta(3 * 365 / 12))

    def ahs_y3_subject_visit(self, ahs_y2_household_member):
        """Return an ahs  year 3 subject visit."""
        # Create an ahs member
        survey = site_surveys.current_surveys[2]
        household_member = super().make_ahs_household_member(ahs_y2_household_member, survey)
        appointment = Appointment.objects.get(
            subject_identifier=household_member.subject_identifier,
            visit_code=T2)

        return mommy.make_recipe(
            'bcpp_subject.subjectvisit',
            household_member=household_member,
            subject_identifier=household_member.subject_identifier,
            appointment=appointment,
            report_datetime=self.get_utcnow() + datetime.timedelta(2 * 365 / 12))

    def test_no_circumsition_in_y2(self):
        """Assert that circumcision forms are not required at ahs if filled at bhs."""
        mommy.make_recipe(
            'bcpp_subject.circumcision',
            subject_visit=self.bhs_subject_visit_male,
            circumcised=YES,
            report_datetime=self.get_utcnow()
        )
        mommy.make_recipe(
            'bcpp_subject.circumcised',
            subject_visit=self.bhs_subject_visit_male,
            report_datetime=self.get_utcnow(),
            where_circ='Lobatse',
            why_circ='not_sure'
        )

        # Create a year 2 subject visit.
        self.ahs_subject_visit()

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.circumcision', NOT_REQUIRED, self.visit_code_T1).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.circumcised', NOT_REQUIRED, self.visit_code_T1).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.uncircumcised', NOT_REQUIRED, self.visit_code_T1).count(), 1)

    def test_pos_in_y1_no_hiv_forms(self):
        """Assert that is a participant is positive in year 1 hiv forms are not required the following year."""
        self._hiv_result = self.hiv_result(POS, self.bhs_subject_visit_male, self.bhs_subject_visit_male.report_datetime)

        # Create a year 2 subject visit.
        self.ahs_y2_subject_visit()

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestreview', NOT_REQUIRED, T1).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtested', NOT_REQUIRED, T1).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresultdocumentation', NOT_REQUIRED, T1).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivtestinghistory', NOT_REQUIRED, T1).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T1).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T1, MICROTUBE).count(), 1)

    def test_hic_filled_in_y1_not_required_in_annual(self):
        """Assert that hic will not be required at year 1 if filled at bhs."""
        self.make_subject_locator(self.subject_identifier, self.bhs_subject_visit_male.report_datetime)
        self.make_residency_mobility(self.bhs_subject_visit_male, YES, NO, self.bhs_subject_visit_male.report_datetime)
        self.hiv_result(NEG, self.bhs_subject_visit_male, self.bhs_subject_visit_male.report_datetime)

        self.make_hic_enrolment(self.bhs_subject_visit_male, YES, self.bhs_subject_visit_male.report_datetime)

        subject_visit_male_y2 = self.ahs_y2_subject_visit()
        self.hiv_result(NEG, subject_visit_male_y2, subject_visit_male_y2.report_datetime)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hicenrollment', NOT_REQUIRED, T1).count(), 1)

        subject_visit_male_y3 = self.ahs_y3_subject_visit(subject_visit_male_y2.household_member)

        self.hiv_result(NEG, subject_visit_male_y3, subject_visit_male_y3.report_datetime)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hicenrollment', NOT_REQUIRED, T2).count(), 1)

    def test_microtube_always_required_for_hic_without_pos_hivresult(self):
        """ Tests that an HIC enrollee who sero-converted to POS status, but the POS result not tested by BHP,
            will be tested by BHP at next visit. """

        self.make_subject_locator(self.subject_identifier, self.bhs_subject_visit_male.report_datetime)

        self.hiv_result(NEG, self.bhs_subject_visit_male, self.bhs_subject_visit_male.report_datetime)

        self.make_residency_mobility(self.bhs_subject_visit_male, YES, NO, self.bhs_subject_visit_male.report_datetime)

        self.make_hic_enrolment(self.bhs_subject_visit_male, YES, self.bhs_subject_visit_male.report_datetime)

        ahs_subject_visit_male_y2 = self.ahs_y2_subject_visit()
#         self.make_hivcareadherence(ahs_subject_visit_male_y2, report_datetime)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', REQUIRED, T1).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, MICROTUBE).count(), 1)
        # Make participant known positive in year 2, microtube and hiv result should remain required
        # NOTE: We are using HivTestingHistory and HivTestReview to create the POS status because the participant
        # was not tested by BHP, they became POS after our last visit with them.
        self.make_hivtesting_history(ahs_subject_visit_male_y2, YES, YES, POS, NO, report_datetime=ahs_subject_visit_male_y2.report_datetime)

        self.hivtest_review(ahs_subject_visit_male_y2, POS, report_datetime=ahs_subject_visit_male_y2.report_datetime)

        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, MICROTUBE).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', REQUIRED, T1).count(), 1)

    def test_microtube_not_required_for_hic_with_pos_hivresult(self):
        """ Tests that an HIC enrollee who sero-converted to POS status, tested by BHP, will not be tested
            again in next visit."""
        self.make_subject_locator(self.subject_identifier, self.bhs_subject_visit_male.report_datetime)

        self.hiv_result(NEG, self.bhs_subject_visit_male)

        self.make_residency_mobility(self.bhs_subject_visit_male, YES, NO, self.bhs_subject_visit_male.report_datetime)

        self.make_hic_enrolment(self.bhs_subject_visit_male, YES, self.bhs_subject_visit_male.report_datetime)

        subject_visit_male_y2 = self.ahs_y2_subject_visit()
        # Make participant known positive in year 2, tested by BHP. That means hey have an HivResult record with POS
        # NOTE: We are using HivResult to indicate that the HIV POS result was tested by BHP.
        self.hiv_result(POS, self.ahs_subject_visit_male_y2, subject_visit_male_y2.report_datetime)

        # We are now in year 3 in which the participant is a known POS.
        self.ahs_y3_subject_visit(subject_visit_male_y2.household_member)

        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T2, MICROTUBE).count(), 1)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T2).count(), 1)

    def test_hiv_pos_requisitions_y2(self):
        """ HIV Negative and in HIC at T0 and Tests Positive during home visits at T1 and is Not on ART at T1.
            Sero Converter, Should offer POC CD4, RBD and VL.
        """
        self.make_subject_locator(self.subject_identifier, self.bhs_subject_visit_male.report_datetime)

        self.make_residency_mobility(self.bhs_subject_visit_male, YES, NO)

        self.hiv_result(NEG, self.bhs_subject_visit_male, self.bhs_subject_visit_male.report_datetime)

        self.make_hic_enrolment(self.bhs_subject_visit_male, YES, self.bhs_subject_visit_male.report_datetime)

        subject_visit_male_y2 = self.ahs_y2_subject_visit()

        self.hiv_result(POS, subject_visit_male_y2, subject_visit_male_y2.report_datetime)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T1).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, VIRAL_LOAD).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, RESEARCH_BLOOD_DRAW).count(), 1)

    def test_Known_hiv_pos_y2_not_hic_require_no_testing(self):

        # They were NEG in year 1
        self.hiv_result(POS, self.bhs_subject_visit_male, self.bhs_subject_visit_male.report_datetime)

        ahs_subject_visit_male_y2 = self.ahs_y2_subject_visit()

        self.make_hivtesting_history(ahs_subject_visit_male_y2, YES, YES, POS, NO, ahs_subject_visit_male_y2.report_datetime)

        self.hivtest_review(ahs_subject_visit_male_y2, POS, ahs_subject_visit_male_y2.report_datetime)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T1).count(), 1)

        self.ahs_subject_visit_male_y3 = self.ahs_y3_subject_visit(ahs_subject_visit_male_y2.household_member)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T2).count(), 1)

    def test_Known_hiv_pos_y3_not_hic_require_no_testing_missed_y2(self):

        # Known POS in T0
        self.make_hivtesting_history(
            self.bhs_subject_visit_male, YES, YES, POS, NO, self.bhs_subject_visit_male.report_datetime)

        self.hivtest_review(self.bhs_subject_visit_male, POS, self.bhs_subject_visit_male.report_datetime)

        ahs_subject_visit_male_y2 = self.ahs_y2_subject_visit()

        # Misses T1, and is seen again at T2. They should not be Tested.
        self.ahs_subject_visit_male_y3 = self.ahs_y3_subject_visit(ahs_subject_visit_male_y2.household_member)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivresult', NOT_REQUIRED, T2).count(), 1)

    def test_hic_enrolled_at_bhs(self):
        """ If there is an hic record at bhs then at ahs inspect the record then check for hic status if not enrolled then Hic_enrollment
            should be filled otherwise should not be filled.
        """
        self.make_subject_locator(self.subject_identifier, self.bhs_subject_visit_male.report_datetime)

        self.make_residency_mobility(self.bhs_subject_visit_male, YES, NO, self.bhs_subject_visit_male.report_datetime)

        self.hiv_result(NEG, self.bhs_subject_visit_male, self.bhs_subject_visit_male.report_datetime)

        self.make_hic_enrolment(self.bhs_subject_visit_male, YES, self.bhs_subject_visit_male.report_datetime)

        self.ahs_y2_subject_visit()

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hicenrollment', NOT_REQUIRED, T1).count(), 1)

        self.ahs_y2_subject_visit()

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hicenrollment', NOT_REQUIRED, T2).count(), 1)

    def test_hic_not_enrolled_at_bhs(self):
        """ If there is an hic record inspect the record then check for hic status if not enrolled then Hic_enrollment
            should be offered again at T1.
        """
        self.make_subject_locator(self.subject_identifier, self.bhs_subject_visit_male.report_datetime)

        self.make_residency_mobility(self.bhs_subject_visit_male, YES, NO, self.bhs_subject_visit_male.report_datetime)

        self.hiv_result(NEG, self.bhs_subject_visit_male, self.bhs_subject_visit_male.report_datetime)

        self.make_hic_enrolment(self.bhs_subject_visit_male, NO, self.bhs_subject_visit_male.report_datetime)

        ahs_subject_visit_male_y2 = self.ahs_y2_subject_visit()

        self.hiv_result(NEG, ahs_subject_visit_male_y2, ahs_subject_visit_male_y2.report_datetime)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hicenrollment', REQUIRED, T1).count(), 1)

    def test_hiv_pos_nd_art_naive_at_ahs_new_erollee(self):
        """New enrollees at T0 (i.e doing BHS procedures) who are HIV-positive and ART naive, then PIMA required.
        """
        ahs_subject_visit_male_y2 = self.ahs_y2_subject_visit()

        # Known POS in T0
        self.make_hivtesting_history(self.ahs_subject_visit_male_y2, YES, YES, POS, NO, ahs_subject_visit_male_y2.report_datetime)

        self.hivtest_review(ahs_subject_visit_male_y2, POS, ahs_subject_visit_male_y2.report_datetime)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.ahs_subject_visit_male_y2, NO, NO, NO, NO, NO, ahs_subject_visit_male_y2.report_datetime)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T1).count(), 1)

    def test_hiv_pos_nd_art_naive_at_ahs(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART, (i.e arv_naive) at the time of enrollment.
           Still arv_naive at AHS. Pima and VL required. RBD keyed in T0, so not required.
        """
        self.hiv_pos_nd_art_naive_at_bhs()

        ahs_subject_visit_male_y2 = self.ahs_y2_subject_visit()

        # add HivCarAdherence,
        self.make_hiv_care_adherence(ahs_subject_visit_male_y2, NO, YES, NO, NO, NO, ahs_subject_visit_male_y2.report_datetime)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T1).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, VIRAL_LOAD).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T1, RESEARCH_BLOOD_DRAW).count(), 1)

    def test_hiv_pos_nd_on_art_at_ahs(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART (i.e arv_naive) at the time of enrollment.
           But now on ART at T1. Pima and VL required at T1(rule: art naive at enrollment).
           RBD keyed in T0, so not required. POC VL not required at T1.
        """
        self.subject_identifier = self.bhs_subject_visit_male.subject_identifier

        # Known POS in T0
        self.make_hivtesting_history(self.bhs_subject_visit_male, YES, YES, POS, NO)

        self.hivtest_review(self.bhs_subject_visit_male, POS)

        self.make_hiv_care_adherence(self.bhs_subject_visit_male, YES, YES, YES, YES, YES)

        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T0, RESEARCH_BLOOD_DRAW).count(), 1)

        self.make_requisition(self.bhs_subject_visit, RESEARCH_BLOOD_DRAW)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.bhs_subject_visit_male, NO, YES, NO, NO, NO)

        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.bhs_subject_visit_male, report_datetime=self.get_utcnow(),
            panel_name=RESEARCH_BLOOD_DRAW,
        )

        self.ahs_subject_visit_male_y2 = None # self.annual_subject_visit_y2

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.ahs_subject_visit_male_y2, NO, YES, NO, NO, NO)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T1).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, VIRAL_LOAD).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T1, RESEARCH_BLOOD_DRAW).count(), 1)

        self.ahs_subject_visit_male_y3 = None

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.ahs_subject_visit_male_y3, YES, YES, YES, YES, YES)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T2).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T2, VIRAL_LOAD).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T2, RESEARCH_BLOOD_DRAW).count(), 1)

    def test_hiv_pos_nd_on_art_at_y3_missed_y2(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART (i.e arv_naive) at the time of enrollment.
           Misses T1. But now on ART at T2. Pima and VL required at T2(rule: art naive at enrollment).
           RBD keyed in T0, so not required. POC VL not required at T2.
        """
        self.subject_identifier = self.bhs_subject_visit_male.subject_identifier

        # Known POS in T0
        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            subject_visit=self.bhs_subject_visit_male,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )
        mommy.make_recipe(
            'bcpp_subject.hivtestreview',
            report_datetime=self.get_utcnow(),
            subject_visit=self.bhs_subject_visit_male,
            hiv_test_date=self.get_utcnow() - timedelta(days=50),
            recorded_hiv_result=POS)

        # add HivCarAdherence,
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.bhs_subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=YES,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.bhs_subject_visit_male, report_datetime=self.get_utcnow(),
            panel_name=RESEARCH_BLOOD_DRAW,
        )

        self.ahs_subject_visit_male_y3 = None  # self.annual_subject_visit_y3

        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.bhs_subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=YES,
            ever_recommended_arv=YES,
            ever_taken_arv=YES,
            on_arv=YES,
            arv_evidence=YES,  # this is the rule field
        )
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T2).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T2, VIRAL_LOAD).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T2, RESEARCH_BLOOD_DRAW).count(), 1)

    def test_hiv_pos_nd_not_on_art_at_ahs(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART (i.e art_naive) at the time of enrollment. Pima required.
           Still HIV Positive and still not on ART at T1: Should offer POC CD4 and VL. No RBD
        """
        # Known POS in T0
        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            subject_visit=self.bhs_subject_visit_male,
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )
        self.hivtest_review(self.bhs_subject_visit_male, POS)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED, T0).count(), 1)

        # ART naive at the time of enrollment, in this case T0.
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.bhs_subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )
        self.assertEqual(self.requisition_metadata_obj(
            'bcpp_subject.subjectrequisition', NOT_REQUIRED, T0, RESEARCH_BLOOD_DRAW).count(), 1)

        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.bhs_subject_visit_male, report_datetime=self.get_utcnow(),
            panel_name=RESEARCH_BLOOD_DRAW,
        )
        self.assertEqual(self.requisition_metadata_obj(
            'bcpp_subject.subjectrequisition', KEYED, T0, RESEARCH_BLOOD_DRAW).count(), 1)

        # Move on to the first annual visit.
        self.subject_visit_male = None  # self.annual_subject_visit_y2

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T1).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, VIRAL_LOAD).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T1, RESEARCH_BLOOD_DRAW).count(), 1)

        # Move on to the second annual visit.
        self.ahs_subject_visit_male_y3 = None  #  self.annual_subject_visit_y3

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T2).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T2, VIRAL_LOAD).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T2, RESEARCH_BLOOD_DRAW).count(), 1)

    def test_hiv_pos_nd_not_on_art_at_y3_missed_y2(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART (i.e art_naive) at the time of enrollment. Pima required.
           Misses T1. Found at T2 still HIV Positive and still not on ART: Should offer POC CD4 and VL. No RBD.
        """
        # Known POS in T0
        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            subject_visit=self.bhs_subject_visit_male,
            report_datetime=self.get_utcnow(),
            has_tested=YES,
            when_hiv_test='1 to 5 months ago',
            has_record=YES,
            verbal_hiv_result=POS,
            other_record=NO
        )
        self.hivtest_review(self.bhs_subject_visit, POS)
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED, T0).count(), 1)
        # ART naive at the time of enrollment, in this case T0.
        mommy.make_recipe(
            'bcpp_subject.hivcareadherence',
            first_positive=None,
            subject_visit=self.bhs_subject_visit_male,
            report_datetime=self.get_utcnow(),
            medical_care=NO,
            ever_recommended_arv=NO,
            ever_taken_arv=NO,
            on_arv=NO,
            arv_evidence=NO,  # this is the rule field
        )

        self.assertEqual(self.requisition_metadata_obj(
            'bcpp_subject.subjectrequisition', NOT_REQUIRED, T0, RESEARCH_BLOOD_DRAW).count(), 1)

        self.make_requisition(self.bhs_subject_visit, RESEARCH_BLOOD_DRAW)

        self.assertEqual(self.requisition_metadata_obj(
            'bcpp_subject.subjectrequisition', KEYED, T0, RESEARCH_BLOOD_DRAW).count(), 1)

        # JUMP first annual visit. Move on to the second annual visit.
        self.ahs_subject_visit_male_y3 = None

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T2).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T2, VIRAL_LOAD).count(), 1)
        self.assertEqual(self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T2, RESEARCH_BLOOD_DRAW).count(), 1)

    def test_hiv_pos_nd_on_art_at_ahs1(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART naive at the time of enrollment.
           Pima required.
           HIV Positive not on ART at T1: Should offer POC CD4 and VL.
        """
        self.subject_identifier = self.bhs_subject_visit_male.subject_identifier

        self.make_hivtesting_history(self.bhs_subject_visit, YES, YES, POS, NO)

        self.hivtest_review(self.bhs_subject_visit, POS)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.bhs_subject_visit, NO, NO, NO, NO, NO)

        self.ahs_subject_visit_male_y2 = None  # self.annual_subject_visit_y2

        self.make_hiv_care_adherence(self.ahs_subject_visit_male_y2, YES, YES, YES, YES, YES)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T1).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, VIRAL_LOAD).count(), 1)

        self.ahs_subject_visit_male_y3 = None  # self.annual_subject_visit_y3

        self.make_hiv_care_adherence(self.ahs_subject_visit_male_y3, YES, YES, YES, YES, YES)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T1).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, VIRAL_LOAD).count(), 1)

    def test_hiv_pos_nd_not_art_at_y1_misses_y2(self):
        """Previously enrollees at t0 who are HIV-positive but were ART naive at the time of enrollment. Pima required.
           Misses T2. HIV Positive and on ART at T3: Should offer POC CD4 and VL.
        """
        self.make_hivtesting_history(self.bhs_subject_visit_male, YES, YES, POS, NO)
        self.hivtest_review(self.bhs_subject_visit_male, POS)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.bhs_subject_visit_male, NO, NO, NO, NO, NO)

        self.ahs_subject_visit_male_y3 = None

        self.make_hiv_care_adherence(self.ahs_subject_visit_male_y3, YES, YES, YES, YES, YES)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T2).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T2, VIRAL_LOAD).count(), 1)

    def hiv_pos_nd_on_art_bhs(self):
        """Enrollees at t0 who are HIV-positive and on ART at the time of enrollment.
           Pima and POC VL NOT required. RBD, VL required.
        """

        self.hiv_result(POS, self.bhs_subject_visit_male)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.bhs_subject_visit_male, YES, YES, YES, YES, YES)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T0).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T0, VIRAL_LOAD).count(), 1)

        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T0, RESEARCH_BLOOD_DRAW).count(), 1)

    def hiv_pos_nd_on_art_ahs(self):
        """Previously enrollees at t0 who are HIV-positive on ART at the time of enrollment.
           Pima and POC VL NOT required. RBD, VL required.
        """
        self.hiv_pos_nd_on_art_bhs()

        self.ahs_subject_visit_male_y2 = self.annual_subject_visit_y2

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T1).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T1, VIRAL_LOAD).count(), 1)

        self.ahs_subject_visit_male_y3 = None  # self.annual_subject_visit_y3

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T2).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T2, VIRAL_LOAD).count(), 1)

    def test_hiv_neg_bhs_and_pos_at_ahs(self):
        """ HIV Negative and in HIC at T0 and now HIV POS not on ART at T1, should Offer POC CD4, RBD and VL and PIMA VL.
        """
        self.make_residency_mobility(self.bhs_subject_visit_male, YES, NO)

        self.hiv_result(NEG, self.subject_visit_male_T0)

        self.make_subject_locator(self.subject_identifier, self.get_utcnow())

        self.make_hic_enrollment(self.bhs_subject_visit_male, YES, self.get_utcnow())

        self.ahs_subject_visit_male_y2 = None  # self.annual_subject_visit_y2

        self.hiv_result(POS, self.ahs_subject_visit_male_y2)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T1).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, VIRAL_LOAD).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj(
                'bcpp_subject.subjectrequisition', REQUIRED, T1, RESEARCH_BLOOD_DRAW).count(), 1)

    def hiv_pos_at_bhs_and_hiv_care_adherence_is_required(self):
        """Enrollees at t0 who are HIV-positive and on ART at the time of enrollment.
           Pima and POC VL NOT required. RBD, VL required.
        """
        self.hiv_result(POS, self.bhs_subject_visit_male)

        self.ahs_subject_visit_male_y2 = None

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivcareadherence', REQUIRED, T1).count(), 1)

    def test_not_known_pos_runs_hiv_and_cd4_ahs(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""

        self.make_subject_locator(self.subject_identifier, self.get_utcnow())

        self.hiv_result('Declined', self.bhs_subject_visit_male)

        self.ahs_subject_visit_male_y2 = None

        self.hiv_result(POS, self.ahs_subject_visit_male_y2)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T1).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, VIRAL_LOAD).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj(
                'bcpp_subject.subjectrequisition', REQUIRED, T1, RESEARCH_BLOOD_DRAW).count(), 1)

    def test_not_known_neg_runs_hiv_and_cd4_ahs_1(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""

        self.make_subject_locator(self.subject_identifier, self.get_utcnow())

        self.hiv_result(NEG, self.bhs_subject_visit_male)

        self.ahs_subject_visit_male_y2 = None

        self.hiv_result("Declined", self.ahs_subject_visit_male_y2)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T1, VIRAL_LOAD).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj(
                'bcpp_subject.subjectrequisition', NOT_REQUIRED, T1, RESEARCH_BLOOD_DRAW).count(), 1)

    def test_not_known_pos_runs_hiv_and_cd4_ahs_2(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""

        self.make_subject_locator(self.subject_identifier, self.get_utcnow())

        self.hiv_result(POS, self.subject_visit_male_T0)

        self.ahs_subject_visit_male_y2 = None

        self.hiv_result("Declined", self.ahs_subject_visit_male_y2)

        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T1, VIRAL_LOAD).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj(
                'bcpp_subject.subjectrequisition', REQUIRED, T1, RESEARCH_BLOOD_DRAW).count(), 1)

    def test_not_known_pos_runs_hiv_and_cd4_ahs_y3(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""
        self.make_subject_locator(self.subject_identifier, self.get_utcnow())

        self.hiv_result('Declined', self.bhs_subject_visit_male)

        self.make_hivtesting_history(self.bhs_subject_visit_male, "DWTA", "Don't want to answer", "not_answering", NO)

        self.ahs_subject_visit_male_y2 = None

        self.hiv_result('Declined', self.ahs_subject_visit_male_y2)

        self.make_hivtesting_history(
            self.ahs_subject_visit_male_y2, "DWTA", "Don't want to answer", "not_answering", NO)

        self.ahs_subject_visit_male_y3 = None

        self.make_hivtesting_history(
            self.ahs_subject_visit_male_y3, YES, YES, POS, NO)

        self.hiv_result(POS, self.ahs_subject_visit_male_y3)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', REQUIRED, T2).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', REQUIRED, T2, VIRAL_LOAD).count(), 1)

    def test_not_known_neg_runs_hiv_and_cd4_ahs(self):
        """If not a known POS, requires HIV and CD4 (until today's result is known)."""
        self.make_subject_locator(self.subject_identifier, self.get_utcnow())
        self.hiv_result('Declined', self.bhs_subject_visit_male)

        self.ahs_subject_visit_male_y2 = None

        self.hiv_result(NEG, self.ahs_subject_visit_male_y2)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.pima', NOT_REQUIRED, T1).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj('bcpp_subject.subjectrequisition', NOT_REQUIRED, T1, VIRAL_LOAD).count(), 1)
        self.assertEqual(
            self.requisition_metadata_obj(
                'bcpp_subject.subjectrequisition', NOT_REQUIRED, T1, RESEARCH_BLOOD_DRAW).count(), 1)

    def test_hiv_pos_nd_art_naive_at_ahs_require_linkage_to_care(self):
        """Previously enrollees at t0 who are HIV-positive but were not on ART, (i.e arv_naive) at the time of enrollment.
           Still arv_naive at AHS. HIV linkage to care required.
        """
        self.hiv_pos_nd_art_naive_at_bhs()

        self.ahs_subject_visit_male_y2 = None

        self.hiv_result(POS, self.ahs_subject_visit_male_y2)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.ahs_subject_visit_male_y2, NO, YES, YES, YES, YES)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivlinkagetocare', REQUIRED, T1).count(), 1)

    def test_newly_pos_and_not_art_bhs_not_require_linkage_to_care(self):
        """Newly HIV Positive not on ART at T0, Should not offer hiv linkage to care.
        """
        self._hiv_result = self.hiv_result(POS, self.bhs_subject_visit_male)

        self.make_hiv_care_adherence(self.bhs_subject_visit_male, NO, NO, NO, NO, NO)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivlinkagetocare', NOT_REQUIRED, T1).count(), 1)

    def test_pos_on_art_notrequire_linkage_to_care(self):
        """If POS and on arv and have doc evidence, Hiv Linkage to care not required, not a defaulter."""

        self._hiv_result = self.hiv_result(POS, self.bhs_subject_visit_male)

        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.bhs_subject_visit_male, NO, NO, NO, YES, YES)

        # on art so no need for CD
        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivlinkagetocare', NOT_REQUIRED, T0).count(), 1)

    def test_known_neg_does_not_require_linkage_to_care(self):
        """If previous result is NEG, does not require hiv linkage to care.

        See rule_groups.ReviewNotPositiveRuleGroup
        """

        self.ahs_subject_visit_male_y2 = None

        self._hiv_result = self.hiv_result(NEG, self.bhs_subject_visit_male)
        # add HivCarAdherence,
        self.make_hiv_care_adherence(self.bhs_subject_visit_male, NO, NO, NO, YES, YES)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivlinkagetocare', NOT_REQUIRED, T0).count(), 1)

    def test_known_pos_defaulter_require_linkage_to_care(self):
        """If previous result is POS on art but no evidence.

        This is a defaulter

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self.hivtest_review(self.bhs_subject_visit_male, POS)

        # add HivCareAdherence,
        self.make_hiv_care_adherence(self.bhs_subject_visit_male, NO, NO, YES, NO, YES)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivlinkagetocare', REQUIRED, T0).count(), 1)

        self.ahs_subject_visit_male_y2 = self.annual_subject_visit_y2

        # add HivCareAdherence,
        self.make_hiv_care_adherence(self.ahs_subject_visit_male_y2, NO, NO, NO, NO, YES)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivlinkagetocare', NOT_REQUIRED, T0).count(), 1)

    def test_known_pos_not_require_linkage_to_care(self):
        """If previous result is POS on art but no evidence.

        See rule_groups.ReviewNotPositiveRuleGroup
        """

        self.hivtest_review(self.bhs_subject_visit, POS)

        # add HivCareAdherence,
        self.make_hiv_care_adherence(self.bhs_subject_visit_male, NO, NO, YES, YES, YES)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivlinkagetocare', NOT_REQUIRED, T0).count(), 1)

        self.ahs_subject_visit_male_y2 = None

        # add HivCareAdherence,
        self.make_hiv_care_adherence(self.ahs_subject_visit_male_y2, NO, NO, NO, NO, YES)

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivlinkagetocare', NOT_REQUIRED, T1).count(), 1)

    def test_known_neg_does_requires_hiv_linkage_to_care(self):
        """If previous result is NEG, does not need Hiv linkage to care.

        See rule_groups.ReviewNotPositiveRuleGroup
        """
        self._hiv_result = self.hiv_result(NEG, self.bhs_subject_visit_male)

        self.ahs_subject_visit_male_y2 = None

        self.assertEqual(self.crf_metadata_obj('bcpp_subject.hivlinkagetocare', NOT_REQUIRED, T1).count(), 1)
