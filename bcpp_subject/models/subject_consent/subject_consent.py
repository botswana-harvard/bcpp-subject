import re

from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_consent.field_mixins import ReviewFieldsMixin, PersonalFieldsMixin
from edc_consent.field_mixins import SampleCollectionFieldsMixin, CitizenFieldsMixin
from edc_consent.field_mixins import VulnerabilityFieldsMixin
from edc_consent.field_mixins.bw import IdentityFieldsMixin
from edc_consent.managers import ConsentManager
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import YES, NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_map.site_mappers import site_mappers
from edc_search.model_mixins import SearchSlugManager
from member.models import HouseholdMember
from survey.model_mixins import SurveyScheduleModelMixin

from ...managers import SubjectConsentManager
from ...patterns import subject_identifier
from ..model_mixins import SearchSlugModelMixin
from ..utils import is_minor
from .clinic_member_updater import ClinicMemberUpdater
from .updates_or_creates_registration_model_mixin import UpdatesOrCreatesRegistrationModelMixin


class Manager(SubjectConsentManager, SearchSlugManager):
    pass


class SubjectConsent(
        ConsentModelMixin, UpdatesOrCreatesRegistrationModelMixin,
        NonUniqueSubjectIdentifierModelMixin, SurveyScheduleModelMixin,
        IdentityFieldsMixin, ReviewFieldsMixin, PersonalFieldsMixin,
        SampleCollectionFieldsMixin, CitizenFieldsMixin,
        VulnerabilityFieldsMixin, SearchSlugModelMixin, BaseUuidModel):
    """ A model completed by the user that captures the ICF.
    """

    clinic_member_updater_cls = ClinicMemberUpdater

    household_member = models.ForeignKey(
        HouseholdMember, on_delete=models.PROTECT)

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        choices=YES_NO,
        null=True,
        blank=False,
        help_text=('Subject is a minor if aged 16-17. A guardian must '
                   'be present for consent. HIV status may NOT be '
                   'revealed in the household.'),
        editable=False)

    is_signed = models.BooleanField(
        default=False,
        editable=False)

    objects = Manager()

    consent = ConsentManager()

    history = HistoricalRecords()

    def __str__(self):
        return '{0} ({1}) V{2}'.format(
            self.subject_identifier,
            self.survey_schedule_object.name,
            self.version)

    def save(self, *args, **kwargs):

        self.clinic_member_updater_cls(model_obj=self)

        if not self.id:
            self.survey_schedule = self.household_member.survey_schedule_object.field_value
            if re.match(subject_identifier, self.household_member.subject_identifier):
                self.subject_identifier = self.household_member.subject_identifier

        self.study_site = site_mappers.current_map_code
        self.is_minor = YES if is_minor(
            self.dob, self.consent_datetime) else NO
        super().save(*args, **kwargs)

    def natural_key(self):
        return ((self.subject_identifier, self.version,) +
                self.household_member.natural_key())
    natural_key.dependencies = ['bcpp_subject.household_member']

    @property
    def visit_code(self):
        """Returns a value for edc_reference.
        """
        return 'CONSENT'

    @property
    def internal_identifier(self):
        return self.household_member.internal_identifier

    class Meta(ConsentModelMixin.Meta):
        app_label = 'bcpp_subject'
        get_latest_by = 'consent_datetime'
        unique_together = (('subject_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created',)
