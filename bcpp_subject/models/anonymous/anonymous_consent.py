from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_base.utils import age
from edc_consent.field_mixins import PersonalFieldsMixin, SampleCollectionFieldsMixin
from edc_consent.field_mixins.bw import IdentityFieldsMixin
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO
from edc_dashboard.model_mixins import (
    SearchSlugModelMixin as BaseSearchSlugModelMixin, SearchSlugManager)
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin

from bcpp.consents import ANONYMOUS_CONSENT_GROUP
from bcpp.surveys import ANONYMOUS_SURVEY
from member.models import HouseholdMember
from survey.model_mixins import SurveyModelMixin
from survey import S

from ...managers import SubjectConsentManager


def is_minor(dob, reference_datetime):
    return 16 <= age(dob, reference_datetime).years < 18


class SearchSlugModelMixin(BaseSearchSlugModelMixin):

    def get_slugs(self):
        slugs = super().get_slugs()
        return slugs + [
            self.subject_identifier] + self.household_member.get_slugs()

    class Meta:
        abstract = True


class Manager(SubjectConsentManager, SearchSlugManager):
    pass


class AnonymousConsent(
        ConsentModelMixin, UpdatesOrCreatesRegistrationModelMixin,
        NonUniqueSubjectIdentifierModelMixin,
        SurveyModelMixin, IdentityFieldsMixin,
        PersonalFieldsMixin, SampleCollectionFieldsMixin,
        SearchSlugModelMixin,
        BaseUuidModel):

    """ A model completed by the user that captures the ICF.
    """

    household_member = models.ForeignKey(
        HouseholdMember, on_delete=models.PROTECT)

    citizen = models.CharField(
        verbose_name="Are you a Botswana citizen? ",
        max_length=3,
        choices=YES_NO,
        help_text="",
    )

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        null=True,
        blank=False,
        default='-',
        choices=YES_NO,
        help_text=('Subject is a minor if aged 16-17. A guardian must '
                   'be present for consent. '
                   'HIV status may NOT be revealed in the household.'),
        editable=False)

    is_signed = models.BooleanField(default=False, editable=False)

    objects = Manager()

    consent = ConsentManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier, self.version, )

    def __str__(self):
        return '{0} ({1}) V{2}'.format(self.subject_identifier, self.survey, self.version)

    def save(self, *args, **kwargs):
        if not self.id:
            self.survey_schedule = self.household_member.survey_schedule_object.field_value
            self.survey = S(self.survey_schedule_object.field_value,
                            survey_name=ANONYMOUS_SURVEY).survey_field_value
        super().save(*args, **kwargs)

    class Meta(ConsentModelMixin.Meta):
        app_label = 'bcpp_subject'
        consent_group = ANONYMOUS_CONSENT_GROUP
        get_latest_by = 'consent_datetime'
        unique_together = (('subject_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created', )
