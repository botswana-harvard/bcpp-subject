import uuid

from django.test import TestCase, tag
from edc_registration.models import RegisteredSubject
from member.models.household_member.household_member import HouseholdMember

from ..models import ClinicMemberUpdater
from .models import MySubjectConsent


@tag("1")
class TestConsent(TestCase):
    # TODO: finish
    """broken, incomplete"""

    def setUp(self):
        self.identity = '123456789'
        self.subject_identifier = '12345'
        self.registration_identifier = uuid.uuid4()

    def test_clinic_member_updater(self):
        RegisteredSubject.objects.create(
            identity=self.identity,
            subject_identifier=self.subject_identifier,
            registration_identifier=self.registration_identifier)
        HouseholdMember.objects.create(
            internal_identifier=self.registration_identifier)
        obj = MySubjectConsent.objects.create(
            subject_identifier='12345')
        ClinicMemberUpdater(model_obj=obj)
