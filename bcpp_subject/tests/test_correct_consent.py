from django.test import TestCase

from model_mommy import mommy

from faker import Faker

from ..constants import T0

from .test_mixins import SubjectMixin
from bcpp_subject.models.subject_consent import SubjectConsent
from edc_registration.models import RegisteredSubject
from django.core.exceptions import ValidationError

fake = Faker()


class TestCorrectConsent(SubjectMixin, TestCase):

    app_label = 'bcpp_subject'

    def setUp(self):
        super().setUp()
        self.consent_data = {
            'identity': '31721515',
            'confirm_identity': '31721515',
        }
        self.survey_schedule = self.get_survey_schedule(index=0)
        self.bhs_subject_visit_male = self.make_subject_visit_for_consented_subject_male(
            T0, survey_schedule=self.survey_schedule, **self.consent_data)
        self.subject_identifier = self.bhs_subject_visit_male.subject_identifier

    def test_lastname_and_initials(self):
        """Test changing a surname and initials.
        """
        subject_consent = SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier)
        new_last_name = 'DIMSTAR'
        initials = subject_consent.first_name[0] + new_last_name[0]
        mommy.make_recipe(
            'bcpp_subject.correctconsent',
            subject_consent=subject_consent,
            old_last_name=subject_consent.last_name,
            new_last_name=new_last_name,)
        self.assertEqual(subject_consent.last_name, new_last_name)
        self.assertEqual(subject_consent.initials, initials)

    def test_lastname_and_initials2(self):
        """Test changing the surname with the first letter of
        the surname does not change the initials.
        """
        subject_consent = SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier)
        new_last_name = subject_consent.last_name[0] + 'IMSTAR'
        initials = subject_consent.initials
        mommy.make_recipe(
            'bcpp_subject.correctconsent',
            subject_consent=subject_consent,
            old_last_name=subject_consent.last_name,
            new_last_name=new_last_name,)
        self.assertEqual(subject_consent.last_name, new_last_name)
        self.assertEqual(subject_consent.initials, initials)

    def test_lastname_and_initials_registered_subject(self):
        """Test changing a surname and initials updates registered subject.
        """
        subject_consent = SubjectConsent.objects.get(
            subject_identifier=self.subject_identifier)
        new_last_name = 'DIMSTAR'
        initials = subject_consent.first_name[0] + new_last_name[0]
        mommy.make_recipe(
            'bcpp_subject.correctconsent',
            subject_consent=subject_consent,
            old_last_name=subject_consent.last_name,
            new_last_name=new_last_name,)
        try:
            registered_subject = RegisteredSubject.objects.get(
                subject_identifier=subject_consent.subject_identifier)
        except RegisteredSubject.DoesNotExist:
            raise ValidationError("Registered subject can not be missing.")
        else:
            self.assertEqual(registered_subject.last_name, new_last_name)
            self.assertEqual(registered_subject.initials, initials)
