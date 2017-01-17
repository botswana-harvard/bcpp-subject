from model_mommy import mommy
from datetime import date

from django.test import TestCase

from edc_constants.constants import YES, NO, POS,NEG
from edc_constants.constants import NOT_APPLICABLE

from ..forms import HivResultForm
from .test_mixins import SubjectMixin
from bcpp_subject.constants import DECLINED


class TestHivResultForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.consent_data = {
            'identity': '31721515',
            'confirm_identity': '31721515',
            'report_datetime': self.get_utcnow(),
        }
        self.bhs_subject_visit_male = self.make_subject_visit_for_consented_subject_male('T0', **self.consent_data)

        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.bhs_subject_visit_male, report_datetime=self.get_utcnow(),
            panel_name='Microtube',
        )
        mommy.make_recipe(
            'bcpp_subject.subjectlocator', subject_identifier=self.bhs_subject_visit_male.subject_identifier,
            report_datetime=self.get_utcnow(),
        )
        mommy.make_recipe(
            'bcpp_subject.residencymobility', subject_visit=self.bhs_subject_visit_male, report_datetime=self.get_utcnow(),
            permanent_resident=YES,
            intend_residency=NO)

        self.options = {
            'report_datetime': self.get_utcnow(),
            'subject_visit': self.bhs_subject_visit_male.id,
            'hiv_result': NEG,
            'hiv_result_datetime': self.get_utcnow(),
            'blood_draw_type': 'capillary',
            'insufficient_vol': NO,
            'why_not_tested': None,
        }

    def test_form_is_valid(self):
        hiv_result_form = HivResultForm(data=self.options)
        self.assertTrue(hiv_result_form.is_valid())
        self.assertTrue(hiv_result_form.save())

    def test_hiv_test_declined(self):
        """Assert hiv test was declined but no reason was provided."""
        self.options.update(hiv_result=DECLINED, why_not_tested=None, hiv_result_datetime=None)
        hiv_result_form = HivResultForm(data=self.options)
        self.assertFalse(hiv_result_form.is_valid())

    def test_hiv_test_declined_hiv_result_datetime(self):
        """Assert hiv test was declined but test date was provided."""
        self.options.update(hiv_result=DECLINED, why_not_tested='I recently tested', hiv_result_datetime=self.get_utcnow())
        hiv_result_form = HivResultForm(data=self.options)
        self.assertFalse(hiv_result_form.is_valid())

    def test_hiv_test_not_provided(self):
        """Assert hiv test was not performed but reason to decline was provided."""
        self.options.update(hiv_result='Not performed', why_not_tested='I recently tested')
        hiv_result_form = HivResultForm(data=self.options)
        self.assertFalse(hiv_result_form.is_valid())

    def test_no_date_time(self):
        """Assert hiv test was performed but test date not provided."""
        self.options.update(hiv_result_datetime=None)
        hiv_result_form = HivResultForm(data=self.options)
        self.assertFalse(hiv_result_form.is_valid())

    def test_why_not_tested(self):
        """Assert hiv test was performed but reason to decline was provided."""
        self.options.update(why_not_tested='I recently tested')
        hiv_result_form = HivResultForm(data=self.options)
        self.assertFalse(hiv_result_form.is_valid())

    def test_insufficient_volume(self):
        """Assert hiv test was not performed but insufficient_vol value provided."""
        self.options.update(hiv_result='Not performed', insufficient_vol=YES)
        hiv_result_form = HivResultForm(data=self.options)
        self.assertFalse(hiv_result_form.is_valid())

    def test_blood_draw_type(self):
        """Assert blood was drawn but type not indicated."""
        self.options.update(blood_draw_type=NOT_APPLICABLE)
        hiv_result_form = HivResultForm(data=self.options)
        self.assertFalse(hiv_result_form.is_valid())

    def test_blood_draw_type_provided(self):
        """Assert blood draw type was provided but hiv test not performed."""
        self.options.update(hiv_result='Not performed')
        hiv_result_form = HivResultForm(data=self.options)
        self.assertFalse(hiv_result_form.is_valid())

    def test_blood_draw_type_no_volume(self):
        """Assert blood drawn by capillary but insufficient_vol not specified."""
        self.options.update(blood_draw_type='capillary', insufficient_vol=NOT_APPLICABLE)
        hiv_result_form = HivResultForm(data=self.options)
        self.assertFalse(hiv_result_form.is_valid())

    def test_blood_draw_type_with_volume(self):
        """Assert blood drawn type is venous but insufficient_vol is  specified."""
        self.options.update(blood_draw_type='venous', insufficient_vol=YES)
        hiv_result_form = HivResultForm(data=self.options)
        self.assertFalse(hiv_result_form.is_valid())
