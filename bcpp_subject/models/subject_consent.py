from django.apps import apps as django_apps
from django.db import models

from edc_base.model.models.url_mixin import UrlMixin
from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_base.utils import age
from edc_consent.field_mixins.bw import IdentityFieldsMixin
from edc_consent.field_mixins import (
    ReviewFieldsMixin, PersonalFieldsMixin, VulnerabilityFieldsMixin,
    SampleCollectionFieldsMixin, CitizenFieldsMixin)
from edc_consent.model_mixins import ConsentModelMixin
from edc_constants.choices import YES_NO
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_map.site_mappers import site_mappers
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from ..managers import SubjectConsentManager

from member.models import EnrollmentChecklist, HouseholdMember

from ..exceptions import ConsentValidationError

from .model_mixins import SurveyModelMixin


def is_minor(dob, reference_datetime):
    return 16 <= age(dob, reference_datetime).years < 18


class SubjectConsent(
        ConsentModelMixin, UpdatesOrCreatesRegistrationModelMixin, NonUniqueSubjectIdentifierModelMixin,
        SurveyModelMixin, IdentityFieldsMixin, ReviewFieldsMixin,
        PersonalFieldsMixin, SampleCollectionFieldsMixin, CitizenFieldsMixin, VulnerabilityFieldsMixin,
        UrlMixin, BaseUuidModel):

    """ A model completed by the user that captures the ICF."""

    household_member = models.ForeignKey(HouseholdMember, on_delete=models.PROTECT)

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        null=True,
        blank=False,
        default='-',
        choices=YES_NO,
        help_text=('Subject is a minor if aged 16-17. A guardian must be present for consent. '
                   'HIV status may NOT be revealed in the household.'),
        editable=False)

    is_signed = models.BooleanField(default=False, editable=False)

    objects = SubjectConsentManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.subject_identifier, self.version, ) + self.household_member.natural_key()
    natural_key.dependencies = ['bcpp_subject.household_member']

    def __str__(self):
        return '{0} ({1}) V{2}'.format(self.subject_identifier, self.survey, self.version)

    def common_clean(self):
        # confirm member is eligible
        if not self.household_member.eligible_subject:
            raise ConsentValidationError('Member is not eligible for consent')
        # validate dob with HicEnrollment, if it exists
        HicEnrollment = django_apps.get_model('bcpp_subject', 'HicEnrollment')
        try:
            HicEnrollment.objects.get(subject_visit__household_member=self.household_member)
            if self.dob != self.dob:
                raise ConsentValidationError(
                    'Date of birth does not match with that on \'{}\'. Please correct.'.format(
                        HicEnrollment._meta.verbose_name))
        except HicEnrollment.DoesNotExist:
            pass
        # match with enrollment checklist.
        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(
                household_member=self.household_member, is_eligible=True)
        except EnrollmentChecklist.DoesNotExist:
            raise ConsentValidationError(
                'Member has not completed the \'{}\'. Please correct before continuing'.format(
                    EnrollmentChecklist._meta.verbose_name))
        # other model/form validations
        # minor (do this before comparing DoB)
        if YES if is_minor(enrollment_checklist.dob, self.report_datetime) else NO != self.is_minor:
            raise ConsentValidationError(
                'Minor subject mismatch. Subject is a minor based on {enroll} but {consent} says '
                'subject is not a minor. Got {enroll_dob} != {dob} on {consent}'.format(
                    enroll=EnrollmentChecklist._meta.verbose_name,
                    consent=self._meta.verbose_name,
                    enroll_dob=enrollment_checklist.dob.strftime('%Y-%m-%d'),
                    dob=self.dob.strftime('%Y-%m-%d')))
        # match DoB
        if enrollment_checklist.dob != self.dob:
            raise ConsentValidationError(
                'DoB mismatch. DoB does not match \'{}\'. Got {} != {}'.format(
                    EnrollmentChecklist._meta.verbose_name,
                    self.dob.strftime('%Y-%m-%d'), enrollment_checklist.dob.strftime('%Y-%m-%d')))
        # match gender
        if enrollment_checklist.gender != self.gender:
            raise ConsentValidationError(
                'Gender mismatch. Gender does not match \'{}\'. Got {} != {}'.format(
                    EnrollmentChecklist._meta.verbose_name,
                    self.get_gender_display(), enrollment_checklist.get_gender_display()))
        # minor and guardian name
        if enrollment_checklist.guardian == YES and not self.guardian_name:
            raise ConsentValidationError(
                'Minor/Guardian mismatch. Guardian is available based on {} '
                'but guardian name not provided on {}.'.format(
                    EnrollmentChecklist._meta.verbose_name,
                    self._meta.verbose_name))
        elif enrollment_checklist.guardian in [NO, NOT_APPLICABLE] and self.guardian_name:
            raise ConsentValidationError(
                'Minor/Guardian mismatch. Guardian is {} based on {} '
                'but a guardian name is provided on {}.'.format(
                    'not applicable' if enrollment_checklist.guardian == NOT_APPLICABLE else 'not available',
                    EnrollmentChecklist._meta.verbose_name,
                    self._meta.verbose_name))
        # match initials
        if not self.household_member.personal_details_changed == YES:
            if enrollment_checklist.initials != self.initials:
                raise ConsentValidationError('Initials mismatch. Initials do not match \'{}\''.format(
                    EnrollmentChecklist._meta.verbose_name))
        # match citizenship
        if enrollment_checklist.citizen != self.citizen:
            raise ConsentValidationError(
                'Citizenship mismatch. Citizenship does not match \'{}\'. Got {} != {}'.format(
                    EnrollmentChecklist._meta.verbose_name,
                    self.get_citizen_display(), enrollment_checklist.get_citizen_display()))
        # match literacy
        if enrollment_checklist.literacy == YES and self.is_literate != YES:
            raise ConsentValidationError(
                'Literacy mismatch. {} reports subject is literate but {} reports subject is not.'.format(
                    EnrollmentChecklist._meta.verbose_name,
                    self._meta.verbose_name))
        elif enrollment_checklist.literacy == NO and self.is_literate != NO:
            raise ConsentValidationError(
                'Literacy mismatch. {} reports subject is not literate but {} reports subject is.'.format(
                    EnrollmentChecklist._meta.verbose_name,
                    self._meta.verbose_name))
        elif enrollment_checklist.literacy == NO and self.is_literate == NO and not self.witness_name:
            raise ConsentValidationError(
                'Literacy mismatch. Subject is not literate but '
                'no witness name is provided on {}.'.format(
                    self._meta.verbose_name))
        # match marriage if not citizen
        if self.citizen == NO:
            if (enrollment_checklist.legal_marriage != self.legal_marriage) or (
                    enrollment_checklist.marriage_certificate != self.marriage_certificate):
                raise ConsentValidationError(
                    'Citizenship by marriage mismatch. {} reports subject is married '
                    'to a citizen with a valid marriage certificate. This does not match \'{}\''.format(
                        self._meta.verbose_name,
                        EnrollmentChecklist._meta.verbose_name))
        super().common_clean()

    def save(self, *args, **kwargs):
        self.study_site = site_mappers.current_map_code
        self.is_minor = YES if is_minor(self.dob, self.consent_datetime) else NO
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'bcpp_subject'
        get_latest_by = 'consent_datetime'
        unique_together = (('subject_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))
        ordering = ('-created', )
