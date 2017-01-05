from model_mommy import mommy

from django.test import TestCase

from edc_constants.constants import YES, NO

from ..forms import EducationForm
from ..models import SubjectLocator

from .test_mixins import SubjectMixin


class TestEducationForm(SubjectMixin, TestCase):

    def setUp(self):
        super().setUp()
        self.subject_visit = self.make_subject_visit_for_consented_subject('T0')
        mommy.make_recipe(
            'bcpp_subject.subjectlocator', subject_identifier=self.subject_visit.subject_identifier,
            report_datetime=self.get_utcnow(),
        )
        self.options = {
            'report_datetime': self.get_utcnow(),
            'subject_visit': self.subject_visit.id,
            'education': 'Senior Secondary',
            'working': YES,
            'job_type': 'part-time',
            'reason_unemployed': None,
            'job_description': 'farmer',
            'monthly_income': '5000-10,000 pula',
        }

    def test_form_is_valid(self):
        education_form = EducationForm(data=self.options)
        self.assertTrue(education_form.is_valid())

    def test_permission_to_contact_at_work(self):
        """Assert participant consented to be contacted at work is working."""
        subject_locator = SubjectLocator.objects.get(
            subject_identifier=self.subject_visit.subject_identifier)
        subject_locator.may_call_work = YES
        subject_locator.save_base(update_fields=['may_call_work'])

        self.options.update(working=NO)
        education_form = EducationForm(data=self.options)
        self.assertFalse(education_form.is_valid())

    def test_retired_without_benefits(self):
        self.options.update(reason_unemployed='retired', monthly_income=None)
        education_form = EducationForm(data=self.options)
        self.assertFalse(education_form.is_valid())

    def test_student_without_benefits(self):
        self.options.update(reason_unemployed='student', monthly_income=None)
        education_form = EducationForm(data=self.options)
        self.assertFalse(education_form.is_valid())

    def test_working_with_unemployed_reasons(self):
        self.options.update(reason_unemployed='waiting')
        education_form = EducationForm(data=self.options)
        self.assertFalse(education_form.is_valid())

    def test_working_with_no_job_type(self):
        self.options.update(job_type=None)
        education_form = EducationForm(data=self.options)
        self.assertFalse(education_form.is_valid())

    def test_working_with_no_job_description(self):
        self.options.update(job_description=None)
        education_form = EducationForm(data=self.options)
        self.assertFalse(education_form.is_valid())

    def test_working_with_no_monthly_income(self):
        self.options.update(monthly_income=None)
        education_form = EducationForm(data=self.options)
        self.assertFalse(education_form.is_valid())

    def test_not_working_with_job_type(self):
        self.options.update(working=NO, job_type=None)
        education_form = EducationForm(data=self.options)
        self.assertFalse(education_form.is_valid())

    def test_not_working_with_job_description(self):
        self.options.update(working=NO, job_description=None)
        education_form = EducationForm(data=self.options)
        self.assertFalse(education_form.is_valid())

    def test_not_working_with_no_reasons_unemployed(self):
        self.options.update(working=NO, reason_unemployed=None)
        education_form = EducationForm(data=self.options)
        self.assertFalse(education_form.is_valid())
