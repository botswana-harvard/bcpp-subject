import arrow

from model_mommy import mommy

from django.test import TestCase

from edc_constants.constants import NEG, YES, NO
from edc_base_test.utils import get_utcnow

from .test_mixins import SubjectMixin
from bcpp_subject.forms.hic_enrollment_form import HicEnrollmentForm
from dateutil.relativedelta import relativedelta
from bcpp_subject.models.residency_mobility import ResidencyMobility


class TestHicEnrollmentForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')

        mommy.make_recipe(
            'bcpp_subject.subjectlocator', subject_identifier=self.subject_visit.subject_identifier, report_datetime=get_utcnow(),
        )
        mommy.make_recipe(
            'bcpp_lab.subjectrequisition', subject_visit=self.subject_visit, report_datetime=get_utcnow(),
            panel_name='Microtube',
        )
        mommy.make_recipe(
            'bcpp_subject.hivresult', subject_visit=self.subject_visit, report_datetime=get_utcnow(),
            hiv_result=NEG
        )
        mommy.make_recipe(
            'bcpp_subject.residencymobility', subject_visit=self.subject_visit, report_datetime=get_utcnow(),
            permanent_resident=YES,
            intend_residency=NO)
        self.options = {
            'hic_permission': YES,
            'hiv_status_today': NEG,
            'consent_datetime': get_utcnow(),
            'report_datetime': get_utcnow(),
            'subject_visit': self.subject_visit.id,
            'dob': (arrow.utcnow() - relativedelta(years=19)).date(),
            'permanent_resident': YES
        }
        form = HicEnrollmentForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_is_permanent_resident(self):
        """ IF residency mobility record exists then hic enrollment expects permanent_resident to be YES. """
        residencymobility = ResidencyMobility.objects.get(subject_visit=self.subject_visit)
        residencymobility.permanent_resident = NO
        residencymobility.save()
        form = HicEnrollmentForm(data=self.options)
        self.assertFalse(form.is_valid())

        residencymobility.permanent_resident = YES
        residencymobility.save()
        form = HicEnrollmentForm(data=self.options)
        self.assertTrue(form.is_valid())

    def test_is_intended_residency(self):
        """ IF residency mobility record exists then hic enrollment expects intend_residency to be NO. """
        residencymobility = ResidencyMobility.objects.get(subject_visit=self.subject_visit)
        residencymobility.intend_residency = YES
        residencymobility.save()
        form = HicEnrollmentForm(data=self.options)
        self.assertFalse(form.is_valid())

        residencymobility.intend_residency = NO
        residencymobility.save()
        form = HicEnrollmentForm(data=self.options)
        self.assertTrue(form.is_valid())
