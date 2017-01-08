import arrow

from model_mommy import mommy

from dateutil.relativedelta import relativedelta
from django.test import TestCase

from edc_constants.constants import NEG, YES, NO, POS
from edc_base_test.utils import get_utcnow

from .test_mixins import SubjectMixin

from member.models.enrollment_checklist import EnrollmentChecklist

from bcpp_subject.forms.hic_enrollment_form import HicEnrollmentForm
from bcpp_subject.models import SubjectLocator, HivResult, SubjectConsent, ResidencyMobility


class TestHicEnrollmentForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')

        mommy.make_recipe(
            'bcpp_subject.subjectlocator', subject_identifier=self.subject_visit.subject_identifier,
            report_datetime=get_utcnow(),
        )
        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.subject_visit, report_datetime=get_utcnow(),
            panel_name='Microtube',
        )
        mommy.make_recipe(
            'bcpp_subject.subjectrequisition', subject_visit=self.subject_visit, report_datetime=get_utcnow(),
            panel_name='ELISA'
        )
        mommy.make_recipe(
            'bcpp_subject.hivresult', subject_visit=self.subject_visit, report_datetime=get_utcnow(),
            hiv_result=NEG
        )
        mommy.make_recipe(
            'bcpp_subject.elisahivresult', subject_visit=self.subject_visit, report_datetime=get_utcnow(),
            hiv_result=NEG)
        mommy.make_recipe(
            'bcpp_subject.residencymobility', subject_visit=self.subject_visit, report_datetime=get_utcnow(),
            permanent_resident=YES,
            intend_residency=NO)
        self.options = {
            'created': get_utcnow(),
            'modified': get_utcnow(),
            'hostname_created': 'testuser',
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

    def test_if_subject_will_relocate(self):
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

    def test_is_citizen_or_spouse(self):
        enrollment_checklist = EnrollmentChecklist.objects.get(
            household_member__subject_identifier=self.subject_visit.subject_identifier)
        enrollment_checklist.citizen = NO
        enrollment_checklist.legal_marriage = NO
        enrollment_checklist.marriage_certificate = NO
        enrollment_checklist.save_base()

        subject_consent = SubjectConsent.objects.get(subject_identifier=self.subject_visit.subject_identifier)
        subject_consent.citizen = NO
        subject_consent.legal_marriage = NO
        subject_consent.marriage_certificate = NO
        subject_consent.save_base()

        form = HicEnrollmentForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_is_locator_information(self):
        fields = ['subject_cell', 'subject_cell_alt', 'subject_phone', 'mail_address', 'physical_address',
                  'subject_phone_alt', 'subject_work_place', 'subject_work_phone', 'contact_physical_address',
                  'contact_cell', 'contact_phone']
        subject_locator = SubjectLocator.objects.get(subject_identifier=self.subject_visit.subject_identifier)
        for field in fields:
            setattr(subject_locator, field, None)
        subject_locator.save()

        form = HicEnrollmentForm(data=self.options)
        self.assertFalse(form.is_valid())

    def test_get_hiv_status_today(self):
        hiv_result = HivResult.objects.get(subject_visit=self.subject_visit)
        hiv_result.hiv_result = POS
        hiv_result.save()
        form = HicEnrollmentForm(data=self.options)
        self.assertFalse(form.is_valid())
