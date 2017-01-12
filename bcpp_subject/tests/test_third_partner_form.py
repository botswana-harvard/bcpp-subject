from django.test.testcases import TestCase
from bcpp_subject.tests.test_mixins import SubjectMixin
from edc_constants.constants import FEMALE, DONT_KNOW, YES, POS, NO, NEG, DWTA,\
    NOT_APPLICABLE
from bcpp_subject.forms.partner_form import ThirdPartnerForm
from bcpp_subject.models.list_models import PartnerResidency
from model_mommy import mommy


class TestThirdPartnerForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')

        mommy.make_recipe(
            'bcpp_subject.sexualbehaviour',
            subject_visit=self.subject_visit,
            report_datetime=self.get_utcnow(),lifetime_sex_partners=1,
        )
        self.options = {
            'rel_type': 'Casual',
            'first_partner_cp': YES,
            'partner_hiv_test': YES,
            'first_disclose': YES,
            'concurrent': NO,
            'first_first_sex': 'Months',
            'third_last_sex': 'Months',
            'first_haart': YES,
            'first_relationship': 'Boyfriend/Girlfriend',
            'first_first_sex': 'Days',
            'goods_exchange': YES,
            'first_condom_freq': 'All of the time',
            'past_year_sex_freq': 'Less than once a month',
            'first_partner_hiv': POS,
            'first_sex_current': YES,
            'sex_partner_community': 'Ranaka',
            'partner_residency': 'Outside community',
            'first_partner_live': [PartnerResidency.objects.create(name='Outside community').id],
            'first_exchange': '19-29',
            'partner_age': 20,
            'partner_gender': FEMALE,
            'last_sex_contact': 15,
            'last_sex_contact_other': None,
            'first_sex_contact': 20,
            'first_sex_contact_other': None,
            'first_first_sex_calc': 11,
            'regular_sex': 5,
            'having_sex': YES,
            'having_sex_reg': 'Sometimes',
            'alcohol_before_sex': YES,
            'partner_status': POS,
            'partner_arv': DONT_KNOW,
            'status_disclosure': NO,
            'multiple_partners': YES,
            'lifetime_sex_partners': 2,
            'intercourse_type': 'Vaginal',
            'subject_visit': self.subject_visit.id,
            'report_datetime': self.get_utcnow(),
            'created': self.get_utcnow(),
            'modified': self.get_utcnow(),
            'third_last_sex_calc': 12,
            'hostname_created': 'testuser',
        }

    def test_valid_form(self):
        form = ThirdPartnerForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_if_participant_has_one_lifetime_sex_partner(self):
        """Asserts to see if participant has one sex partner"""
        self.options.update(lifetime_sex_partners=1, concurrent=NO)
        form = ThirdPartnerForm(data=self.options)
        self.assertTrue(form.is_valid())

        self.options.update(concurrent=None)
        form = ThirdPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_if_partner_is_hiv_negative(self):
        """Asserts that partners HIV status is negative"""
        self.options.update(first_partner_hiv=POS, first_haart=YES)
        form = ThirdPartnerForm(data=self.options)
        self.assertTrue(form.is_valid())

        self.options.update(first_partner_hiv='negative', first_haart='Yes')
        form = ThirdPartnerForm(data=self.options)
        print(form.errors)
        self.assertFalse(form.is_valid())

    def test_if_partner_hiv_status_not_known(self):
        """Assert that the partners hiv status is unknown"""
        self.options.update(partner_status='I am not sure', first_haart='not_sure')
        form = ThirdPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_third_last_time_of_sex_calc_days(self):
        """Assert that last day of sex was in days not more than 31"""
        self.options.update(third_last_sex='Days', third_last_sex_calc=32)
        form = ThirdPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_third_last_time_of_sex_calc_months(self):
        """Assert that last day of sex was in months not more than 12"""
        self.options.update(third_last_sex='Months', third_last_sex_calc=13)
        form = ThirdPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_first_first_time_of_sex_calc_days(self):
        """Assert that first first day of sex was in days not more than 31"""
        self.options.update(first_first_sex='Days', first_first_sex_calc=32)
        form = ThirdPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_first_first_time_of_sex_calc_months(self):
        """Assert that last day of sex was in months not more than 12"""
        self.options.update(first_first_sex='Months', first_first_sex_calc=13)
        form = ThirdPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_where_first_partner_live(self):
        """Assert to see where first partner lived"""
        self.options.update(sex_partner_community=None)
        form = ThirdPartnerForm(data=self.options)
        self.assertFalse(form.is_valid())
