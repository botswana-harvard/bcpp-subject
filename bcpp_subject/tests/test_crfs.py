from dateutil.relativedelta import relativedelta
from faker import Faker
from model_mommy import mommy

from django.test import TestCase, tag

from edc_appointment.models import Appointment
from edc_base.utils import age
from edc_constants.constants import NO, CONSENTED

from member.constants import ELIGIBLE_FOR_CONSENT, ELIGIBLE_FOR_SCREENING
from member.models import HouseholdMember

from ..exceptions import ConsentValidationError

from .test_mixins import SubjectMixin


fake = Faker()


class TestCrfs(SubjectMixin, TestCase):

    def test_datetime(self):
        self.assertIsNotNone(self.get_utcnow())

#     def test_subject_visit(self):
#         subject_consent = self.make_subject_consent()
#         appointment = Appointment.objects.get(household_member=subject_consent.household_member)
#         mommy.make_recipe(
#             'bcpp_subject.subjectvisit',
#             appointment=appointment)
