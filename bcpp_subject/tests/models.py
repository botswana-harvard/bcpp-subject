from django.db import models
from edc_base.model_mixins.base_uuid_model import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from django.db.models.deletion import PROTECT
from member.models import HouseholdMember


class MySubjectConsent(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    consent_datetime = models.DateTimeField(default=get_utcnow)

    dob = models.DateField(null=True)

    citizen = models.CharField(max_length=25, default=YES)

    legal_marriage = models.CharField(max_length=25, null=True)

    marriage_certificate = models.CharField(max_length=25, null=True)

    identity = models.CharField(max_length=25, default='123456789')

    household_member = models.ForeignKey(HouseholdMember, on_delete=PROTECT)
