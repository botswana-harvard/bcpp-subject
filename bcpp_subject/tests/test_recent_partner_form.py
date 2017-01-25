from model_mommy import mommy

from django.test import TestCase

from edc_constants.constants import YES, NO, NEG, POS, OTHER

from .test_mixins import SubjectMixin
from ..forms import RecentPartnerForm


class TestRecentPartnerForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.consent_data = {
            'identity': '31721516',
            'confirm_identity': '31721516',
        }
        self.ess_subject_visit_male = self.make_subject_visit_for_consented_subject_male(
            'T0', **self.consent_data)

        self.partner_residency = mommy.make_recipe('bcpp_subject.partnerresidency',)

        self.options = {
            'subject_visit': self.ess_subject_visit_male.id,
            'report_datetime': self.get_utcnow(),
            'first_partner_arm': None,
            'first_partner_live': [self.partner_residency.id],
            'sex_partner_community': 'Bokaa',
            'past_year_sex_freq': 'Less than once a month',
            'third_last_sex': 'Days',
            'third_last_sex_calc': None,
            'first_first_sex': 'Days',
            'first_first_sex_calc': None,
            'first_sex_current': YES,
            'first_relationship': 'Long-term partner',
            'first_exchange': '19-29',
            'concurrent': NO,
            'goods_exchange': NO,
            'first_sex_freq': 0,
            'first_partner_hiv': POS,
            'partner_hiv_test': YES,
            'first_haart': NO,
            'first_disclose': YES,
            'first_condom_freq': 'All of the time',
            'first_partner_cp': NO,
            'first_exchange2': 'lte_18',
        }

#     def test_validity(self):
#         form = RecentPartnerForm(data=self.options)
#         print(form.errors)
#         self.assertTrue(form.is_valid())

    def test_first_partner_hiv_neg_first_haart_not_null(self):
        """Assert form is invalid if first partner hiv status is NEG and first haart is not none."""
        self.options.update(
            first_partner_hiv=NEG,
            first_haart=NO)
        form = RecentPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_first_partner_hiv_not_sure_first_haart_not_null(self):
        """Assert form is invalid if first partner hiv status is not sure and first haart is not none."""
        self.options.update(
            first_partner_hiv='I am not sure',
            first_haart=NO)
        form = RecentPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_third_last_sex_days_third_last_sex_calc_grt_31(self):
        """Assert form is invalid if third last sex is Days and the number of days is > 31."""
        self.options.update(
            third_last_sex='Days',
            third_last_sex_calc=32)
        form = RecentPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_third_last_sex_months_third_last_sex_calc_grt_12(self):
        """Assert form is invalid if third last sex is Months and the number of months is > 12."""
        self.options.update(
            third_last_sex='Months',
            third_last_sex_calc=13)
        form = RecentPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_first_sex_days_first_first_sex_calc_grt_31(self):
        """Assert form is invalid if first sex is Days and the number of days is > 31."""
        self.options.update(
            first_first_sex='Days',
            first_first_sex_calc=32)
        form = RecentPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_first_sex_months_first_first_sex_calc_grt_12(self):
        """Assert form is invalid if first sex is Months and the number of days is > 12."""
        self.options.update(
            first_first_sex='Months',
            first_first_sex_calc=13)
        form = RecentPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_first_partner_live_not_null_sex_partner_community_not_applicable(self):
        """Assert form is invalid if first partner is 'In this community' and
           sex partner community is not in NOT_APPLICABLE."""
        self.options.update(
            sex_partner_community='Bokaa')
        form = RecentPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_first_exchange2_no_other_valid(self):
        """Assert precise age not provided for age 19 and older.
        """
        self.options.update(first_exchange2=OTHER, first_exchange2_other=None)
        form = RecentPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_first_exchange2_other_valid(self):
        """Assert precise age not provided for age less than 19.
        """
        self.options.update(first_exchange2_other=20)
        form = RecentPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())
