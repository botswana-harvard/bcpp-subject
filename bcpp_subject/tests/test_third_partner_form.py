from django.test.testcases import TestCase
from bcpp_subject.tests.test_mixins import SubjectMixin
from edc_constants.constants import FEMALE, DONT_KNOW, YES, POS, NO
from bcpp_subject.forms.partner_form import ThirdPartnerForm


class TestThirdPartnerForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')
        self.options = {
            'rel_type': 'Casual',
            'rel_type_other': None,
            'partner_residency': 'In this community',
            'partner_age': 20,
            'partner_gender': FEMALE,
            'last_sex_contact': 15,
            'last_sex_contact_other': None,
            'first_sex_contact': 20,
            'first_sex_contact_other': None,
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
        }

    def test_valid_form(self):
        form = ThirdPartnerForm(data=self.options)
        self.assertTrue(form.is_valid())
