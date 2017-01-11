from django.test.testcases import TestCase
from bcpp_subject.tests.test_mixins import SubjectMixin
from edc_constants.constants import FEMALE, DONT_KNOW, YES, POS, NO, NEG
from bcpp_subject.forms.partner_form import ThirdPartnerForm
from bcpp_subject.models.list_models import PartnerResidency
from model_mommy import mommy


class TestThirdPartnerForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')

        mommy.make_recipe(
            'bcpp_subject.sexualbehaviour', subject_visit=self.subject_visit, report_datetime=self.get_utcnow(),
        )
        self.options = {
            'rel_type': 'Casual',
            'first_partner_cp': YES,
            'partner_hiv_test': YES,
            'first_disclose': YES,
            'concurrent': NO,
            'first_first_sex': 'Months',
            'third_last_sex': 'Months',
            'first_relationship': 'Boyfriend/Girlfriend',
            'goods_exchange': YES,
            'first_condom_freq': 'All of the time',
            'past_year_sex_freq': 'Less than once a month',
            'first_partner_hiv': NEG,
            'first_sex_current': YES,
            'sex_partner_community': 'Ranaka',
            'partner_residency': 'In this community',
            'first_partner_live': [PartnerResidency.objects.create(name='In this community').id],
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
            'intercourse_type': 'Vaginal',
            'subject_visit': self.subject_visit.id,
            'report_datetime': self.get_utcnow(),
            'created': self.get_utcnow(),
            'modified': self.get_utcnow(),
            'hostname_created': 'testuser',
        }

    def test_valid_form(self):
        form = ThirdPartnerForm(data=self.options)
        print(form.errors)
        self.assertTrue(form.is_valid())
