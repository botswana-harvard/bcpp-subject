from datetime import date
from dateutil.relativedelta import relativedelta
from model_mommy import mommy

from django.test import TestCase

from edc_constants.constants import YES, NO, NEG, POS
from edc_map.site_mappers import site_mappers

from bcpp.communities import is_intervention

from .test_mixins import SubjectMixin


class TestReferral(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')

    def tests_referred_hiv(self):
        """if IND refer for HIV testing"""
        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.subject_visit, report_datetime=self.get_utcnow(),
            panel_name='Microtube')
        mommy.make_recipe('bcpp_subject.hivresult', subject_visit=self.subject_visit, hiv_result='IND')
        subject_referral = mommy.make_recipe(
            'bcpp_subject.subjectreferral', subject_referred=YES,
            subject_visit=self.subject_visit, report_datetime=self.get_utcnow(), scheduled_appt_date=self.get_utcnow())
        self.assertIn('', subject_referral.referral_code)

    def referral_smc1(self):
        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.subject_visit, report_datetime=self.get_utcnow(),
            panel_name='Microtube')
        mommy.make_recipe('bcpp_subject.hivresult', subject_visit=self.subject_visit, hiv_result=NEG)
        mommy.make_recipe('bcpp_subject.circumcision', subject_visit=self.subject_visit, circumcised=NO)
        subject_referral = mommy.make_recipe(
            'bcpp_subject.subjectreferral', subject_referred=YES,
            subject_visit=self.subject_visit, report_datetime=self.get_utcnow(), scheduled_appt_date=self.get_utcnow())
        self.assertIn('SMC-NEG', subject_referral.referral_code)

        self.subject_visit_t1 = self.make_subject_visit_for_consented_subject('T1')
        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.subject_visit_t1, report_datetime=self.get_utcnow(),
            panel_name='Microtube')
        mommy.make_recipe('bcpp_subject.hivresult', subject_visit=self.subject_visit_t1, hiv_result=NEG)
        mommy.make_recipe('bcpp_subject.circumcision', subject_visit=self.subject_visit_t1, circumcised=NO)
        subject_referral = mommy.make_recipe(
            'bcpp_subject.subjectreferral', subject_referred=YES,
            subject_visit=self.subject_visit_t1, report_datetime=self.get_utcnow(), scheduled_appt_date=self.get_utcnow())
        return subject_referral

    def tests_referred_smc1(self):
        """if NEG and male and NOT circumcised, refer for SMC in Y1 intervention
        and also refer in Y2 intervention"""
        if is_intervention(site_mappers.current_map_area):
            subject_referral = self.referral_smc1()
            self.assertIn('SMC-NEG', subject_referral.referral_code)

    def tests_referred_smc1a(self):
        """if NEG and male and NOT circumcised, refer for SMC in Y1 non-intervention
        and do not refer in Y2 non-intervention"""
        if not is_intervention(site_mappers.current_map_area):
            subject_referral = self.referral_smc1()
            self.assertEqual('', subject_referral.referral_code)

    def referral_smc2(self):
        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.subject_visit, report_datetime=self.get_utcnow(),
            panel_name='Microtube')
        mommy.make_recipe('bcpp_subject.hivresult', subject_visit=self.subject_visit, hiv_result=NEG)
        mommy.make_recipe('bcpp_subject.circumcision', subject_visit=self.subject_visit, circumcised=YES)
        subject_referral = mommy.make_recipe(
            'bcpp_subject.subjectreferral', subject_referred=YES,
            subject_visit=self.subject_visit, report_datetime=self.get_utcnow(), scheduled_appt_date=self.get_utcnow())
        self.assertNotIn('SMC', subject_referral.referral_code)

        self.subject_visit_t1 = self.make_subject_visit_for_consented_subject('T1')
        subject_referral = mommy.make_recipe(
            'bcpp_subject.subjectreferral', subject_referred=YES,
            subject_visit=self.subject_visit_t1, report_datetime=self.get_utcnow(), scheduled_appt_date=self.get_utcnow())
        return subject_referral

    def tests_referred_smc2(self):
        """if NEG and male and circumcised, do not refer for SMC, both Y1 and Y2 intervention"""
        if is_intervention(site_mappers.current_map_area):
            subject_referral = self.referral_smc2()
            self.assertNotIn('SMC', subject_referral.referral_code)

    def tests_circumsised_y2_not_smc(self):
        """if NEG and male and not circumcised in Y1, then refer for SMC in Y1.
            Then if male circumsised in Y2 then do not refer for SMC in Y2."""
        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.subject_visit, report_datetime=self.get_utcnow(),
            panel_name='Microtube')
        mommy.make_recipe('bcpp_subject.hivresult', subject_visit=self.subject_visit, hiv_result=NEG)
        mommy.make_recipe(
            'bcpp_subject.hivresultdocumentation',
            subject_visit=self.subject_visit,
            result_recorded=NEG,
            result_doc_type='Tebelopele')
        mommy.make_recipe(
            'bcpp_subject.hivtestreview', subject_visit=self.subject_visit, recorded_hiv_result=NEG)
        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory', subject_visit=self.subject_visit, has_tested=YES,
            verbal_hiv_result=NEG,)
        mommy.make_recipe('bcpp_subject.circumcision', subject_visit=self.subject_visit, circumcised=NO)
        subject_referral = mommy.make_recipe(
            'bcpp_subject.subjectreferral', subject_referred=YES,
            subject_visit=self.subject_visit, report_datetime=self.get_utcnow(), scheduled_appt_date=self.get_utcnow())
        self.assertIn('SMC', subject_referral.referral_code)

        self.subject_visit_t1 = self.make_subject_visit_for_consented_subject('T1')
        mommy.make_recipe('bcpp_subject.circumcision', subject_visit=self.subject_visit, circumcised=YES)
        subject_referral = mommy.make_recipe(
            'bcpp_subject.subjectreferral', subject_referred=YES,
            subject_visit=self.subject_visit_t1, report_datetime=self.get_utcnow(), scheduled_appt_date=self.get_utcnow())
        self.assertNotIn('SMC', subject_referral.referral_code)
