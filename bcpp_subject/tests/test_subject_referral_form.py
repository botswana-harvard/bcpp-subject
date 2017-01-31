from model_mommy import mommy

from django.test import TestCase

from .test_mixins import SubjectMixin
from ..forms.subject_referral_form import SubjectReferralForm
from edc_constants.constants import NO, POS, YES, NOT_APPLICABLE
from ..constants import MICROTUBE
from datetime import timedelta

from ..models.subject_referral import SubjectReferral


class TestSubjectReferralForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        report_datetime = self.subject_visit_female.report_datetime
        mommy.make_recipe(
            'bcpp_subject.subjectlocator',
            report_datetime=report_datetime)

        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.subject_visit_female, report_datetime=report_datetime,
            panel_name=MICROTUBE,
        )
        mommy.make_recipe(
            'bcpp_subject.hivresult', subject_visit=self.subject_visit_female, report_datetime=report_datetime,
            hiv_result=POS, insufficient_vol=NO
        )

        mommy.make_recipe(
            'bcpp_subject.hivtestinghistory',
            subject_visit=self.subject_visit_female,
            report_datetime=report_datetime,
        )

        mommy.make_recipe(
            'bcpp_subject.hivtestreview',
            report_datetime=report_datetime,
            subject_visit=self.subject_visit_female,
            hiv_test_date=self.get_utcnow() - timedelta(days=50),
            recorded_hiv_result=POS)

        self.hivresultdocumentation = mommy.make_recipe(
            'bcpp_subject.hivresultdocumentation', subject_visit=self.subject_visit_female,
            report_datetime=report_datetime
        )
        mommy.make_recipe(
            'bcpp_subject.pima', subject_visit=self.bhs_subject_visit_female,
            report_datetime=report_datetime
        )
        self.options = {
            'report_datetime': self.get_utcnow(),
            'subject_visit': self.bhs_subject_visit_female.id,
            'referral_appt_comment': NOT_APPLICABLE,
            'subject_referred': YES,
            'subject_identifier': self.subject_visit_female.subject_identifier,
            'created': self.get_utcnow(),
            'modified': self.get_utcnow(),
            'hostname_created': 'testuser',
        }

    def test_subject_referral_valid(self):
        form = SubjectReferralForm(data=self.options)
        self.assertTrue(form.is_valid())
        self.assertTrue(form.save())
        self.assertEqual(SubjectReferral.objects.all().count(), 1)

    def test_subject_referral_not_valid(self):
        form = SubjectReferralForm(data=self.options)
        self.assertTrue(form.is_valid())

        self.hivresultdocumentation.delete()
        self.assertTrue(form.is_valid())
