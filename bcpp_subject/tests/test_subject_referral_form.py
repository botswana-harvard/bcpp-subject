from model_mommy import mommy

from django.test import TestCase

from .test_mixins import SubjectMixin
from bcpp_subject.forms.subject_referral_form import SubjectReferralForm


class TestSubjectReferralForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')
        mommy.make_recipe(
            'bcpp_subject.subjectlocator',
            subject_identifier=self.subject_visit.subject_identifier,
            report_datetime=self.subject_visit.report_datetime)

        self.options = {
            'report_datetime': self.get_utcnow(),
            'subject_visit': self.subject_visit.id,
            'referral_appt_comment': '',
            'subject_referred': '',
            'subject_identifier': self.subject_visit.subject_identifier,
        }

    def test_subject_referral_valid(self):
        form = SubjectReferralForm(data=self.options)
        self.assertTrue(form.is_valid())
