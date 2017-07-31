import pytz
import re

from django import forms
from django.conf import settings
from django.forms import ValidationError

from edc_consent.modelform_mixins import ConsentModelFormMixin as BaseConsentModelFormMixin
from edc_constants.constants import NOT_APPLICABLE, YES, NO
from edc_registration.models import RegisteredSubject

from member.constants import HEAD_OF_HOUSEHOLD
from member.models import HouseholdInfo, EnrollmentChecklist, HouseholdMember

from ..models import SubjectConsent, HicEnrollment
from ..patterns import subject_identifier
from ..utils import rbd_household_member

tz = pytz.timezone(settings.TIME_ZONE)


class ConsentModelFormMixin(BaseConsentModelFormMixin, forms.ModelForm):

    def clean(self):
        if 'consent_datetime' in self.cleaned_data:
            if not self.cleaned_data.get('consent_datetime'):
                raise forms.ValidationError(
                    'Please indicate the consent datetime.')
        cleaned_data = super().clean()
        self.validate_with_enrollment_checklist()
        self.validate_with_hic_enrollment()
        self.clean_consent_with_household_member()
        self.clean_citizen_is_citizen()
        self.clean_citizen_is_not_citizen()
        self.validate_identity_with_internal_identifier()
        self.household_info()
        return cleaned_data

    def validate_max_age(self):
        cleaned_data = self.cleaned_data
        is_consented = self._meta.model.objects.filter(
            identity=cleaned_data.get('identity')).exists()
        if self.age:
            if self.age.years > self.consent_config.age_max and not is_consented:
                raise forms.ValidationError(
                    'Subject\'s age is %(age)s. Subject is not eligible for '
                    'consent. Maximum age of consent is %(max)s.',
                    params={
                        'age': self.age.years,
                        'max': self.consent_config.age_max},
                    code='invalid')

    def validate_with_enrollment_checklist(self):
        household_member = self.cleaned_data.get('household_member')
        initials = self.cleaned_data.get('initials')
        dob = self.cleaned_data.get('dob')
        gender = self.cleaned_data.get('gender')
        citizen = self.cleaned_data.get('citizen')
        is_literate = self.cleaned_data.get('is_literate')
        witness_name = self.cleaned_data.get('witness_name')
        guardian_name = self.cleaned_data.get('guardian_name')

        try:
            enrollment_checklist = EnrollmentChecklist.objects.get(
                household_member=household_member)
        except EnrollmentChecklist.DoesNotExist:
            raise forms.ValidationError(
                'Please complete \'{}\' first.'.format(
                    EnrollmentChecklist._meta.verbose_name))

        if not enrollment_checklist.is_eligible:
            raise forms.ValidationError(
                'Member did not pass eligibility criteria. See \'{}\'.'.format(
                    EnrollmentChecklist._meta.verbose_name))
        elif enrollment_checklist.initials != initials:
            raise forms.ValidationError({
                'initials': 'Does not match \'{}\'.'.format(
                    EnrollmentChecklist._meta.verbose_name)})
        elif enrollment_checklist.gender != gender:
            raise forms.ValidationError({
                'gender': 'Does not match \'{}\'.'.format(
                    EnrollmentChecklist._meta.verbose_name)})
        elif dob and enrollment_checklist.dob != dob:
            raise forms.ValidationError({
                'dob': 'Does not match \'{}\'. Expected {}.'.format(
                    EnrollmentChecklist._meta.verbose_name,
                    enrollment_checklist.dob.strftime('%Y-%m-%d'))})
        elif enrollment_checklist.citizen != citizen:
            raise forms.ValidationError({
                'citizen': 'Does not match \'{}\'.'.format(
                    EnrollmentChecklist._meta.verbose_name)})
        elif (enrollment_checklist.literacy != is_literate
              and not witness_name):
            raise forms.ValidationError({
                'is_literate': 'Does not match \'{}\'.'.format(
                    EnrollmentChecklist._meta.verbose_name)})
        elif is_literate == NO and not witness_name:
            raise forms.ValidationError({
                'witness_name': 'Witness name is required'})
        elif enrollment_checklist.guardian == YES and not guardian_name:
            raise forms.ValidationError({
                'guardian_name': 'Expected guardian name. See {}.'.format(
                    EnrollmentChecklist._meta.verbose_name)})
        elif enrollment_checklist.guardian in [NO, NOT_APPLICABLE] and guardian_name:
            raise forms.ValidationError({
                'guardian_name': 'Guardian name not expected. See {}.'.format(
                    EnrollmentChecklist._meta.verbose_name)})

    def validate_with_hic_enrollment(self):
        household_member = self.cleaned_data.get("household_member")
        dob = self.cleaned_data.get('dob')
        if dob:
            try:
                hic_enrollment = HicEnrollment.objects.get(
                    subject_visit__household_member=household_member)
            except HicEnrollment.DoesNotExist:
                pass
            else:
                if hic_enrollment.dob != dob:
                    raise forms.ValidationError({
                        'dob': 'Does not match \'{}\'.'.format(
                            HicEnrollment._meta.verbose_name)})

    def validate_identity_with_internal_identifier(self):
        household_member = self.cleaned_data.get('household_member')
        identity = self.cleaned_data.get('identity')
        try:
            registered_subject = RegisteredSubject.objects.get(
                registration_identifier=household_member.internal_identifier)
        except RegisteredSubject.DoesNotExist:
            pass
        else:
            if registered_subject.identity != identity:
                raise forms.ValidationError(
                    {'identity': 'Identity does not match this subject. '
                     'Expected {}.'.format(registered_subject.identity)})


#     def clean_consent_matches_enrollment(self):
#         household_member = self.cleaned_data.get("household_member")
#         if not SubjectConsent.objects.filter(
#                 household_member__internal_identifier=household_member.internal_identifier).exclude(
#                 household_member=household_member).exists():
#             consent_datetime = self.cleaned_data.get(
#                 "consent_datetime", self.instance.consent_datetime)
#             options = deepcopy(self.cleaned_data)
#             options.update({'consent_datetime': consent_datetime})
#             self.instance.matches_enrollment_checklist(
#                 SubjectConsent(**options), forms.ValidationError)
#             self.instance.matches_hic_enrollment(
# SubjectConsent(**options), household_member, forms.ValidationError)

    def clean_consent_with_household_member(self):
        """Validates subject consent values against household
        member values.
        """
        initials = self.cleaned_data.get("initials")
        first_name = self.cleaned_data.get("first_name")
        gender = self.cleaned_data.get("gender")
        household_member = self.cleaned_data.get("household_member")
        if household_member:
            if initials != household_member.initials:
                raise forms.ValidationError({
                    'initials':
                    'Initials do not match with household member. {} <> {}'.format(
                        initials, household_member.initials)})
            if household_member.first_name != first_name:
                raise forms.ValidationError({
                    'first_name': 'First name does not match with household member. '
                    'Got {} <> {}'.format(
                        household_member.first_name, first_name)})
            if household_member.gender != gender:
                raise forms.ValidationError({
                    'gender': 'Gender does not match with household member. '
                    'Got %(gender)s <> %(hm_gender)s'.format(
                        household_member.gender, gender)})

    def clinic_member_consent(self, ess_member, identity):
        """Link a member being consented to a clinic member.
        """
        registered_subject = RegisteredSubject.objects.get(identifier=identity)
        ess_member_dob = EnrollmentChecklist.objects.get(
            household_member=ess_member).dob
        if (ess_member.first_name == registered_subject.first_name and
            ess_member.last_name == registered_subject.last_name and
            ess_member.gender == registered_subject.gender and
                ess_member_dob == registered_subject.dob):
            pass

    def clean_identity_with_unique_fields(self):
        """Overrides default."""
        exclude_options = {}
        household_member = self.cleaned_data.get('household_member')
        identity = self.cleaned_data.get('identity')
        first_name = self.cleaned_data.get('first_name')
        initials = self.cleaned_data.get('initials')
        dob = self.cleaned_data.get('dob')

        existing_rbd_household_member = rbd_household_member(identity=identity)
        if existing_rbd_household_member:
            household_member.internal_identifier = existing_rbd_household_member.internal_identifier
            household_member.save()
            household_member = HouseholdMember.objects.get(
                id=household_member.id)
            try:
                registered_subject = RegisteredSubject.objects.get(
                    identity=identity)
            except RegisteredSubject.DoesNotExist:
                raise forms.ValidationError(
                    f'{RegisteredSubject._meta.verbose_name} should exist.')
            self.cleaned_data.update(
                household_member=household_member,
                subject_identifier=registered_subject.subject_identifier)

        unique_together_form = self.unique_together_string(
            first_name, initials, dob)
        if re.match(subject_identifier, household_member.subject_identifier):
            exclude_options = {
                'subject_identifier': household_member.subject_identifier}
        for consent in self._meta.model.objects.filter(
                identity=identity).exclude(**exclude_options):
            unique_together_model = self.unique_together_string(
                consent.first_name, consent.initials, consent.dob)
            if not self.personal_details_changed:
                if unique_together_form != unique_together_model:
                    raise ValidationError({
                        'identity':
                        'Identity {} is already in use by subject {}. '
                        'Please resolve.'.format(
                            identity, consent.subject_identifier)})
        for consent in self._meta.model.objects.filter(
                first_name=first_name, initials=initials, dob=dob):
            if consent.identity != identity:
                raise ValidationError({
                    'identity':
                    'Subject\'s identity was previously reported as \'{}\'. '
                    'You wrote \'{}\'. Please resolve.'.format(
                        consent.identity, identity)})

    def clean_citizen_is_not_citizen(self):
        citizen = self.cleaned_data.get('citizen')
        legal_marriage = self.cleaned_data.get('legal_marriage')
        marriage_certificate = self.cleaned_data.get('marriage_certificate')
        marriage_certificate_no = self.cleaned_data.get(
            'marriage_certificate_no')
        if citizen == NO:
            if legal_marriage == NOT_APPLICABLE:
                raise forms.ValidationError({
                    'legal_marriage':
                    'You wrote subject is NOT a citizen. Is the subject '
                    'legally married to a citizen?'})
            elif legal_marriage == NO:
                raise forms.ValidationError({
                    'legal_marriage':
                    'You wrote subject is NOT a citizen and is NOT legally '
                    'married to a citizen. Subject cannot be consented'})
            elif legal_marriage == YES and marriage_certificate != YES:
                raise forms.ValidationError({
                    'marriage_certificate':
                    'You wrote subject is NOT a citizen. Subject needs to '
                    'produce a marriage certificate'})
            elif legal_marriage == YES and marriage_certificate == YES:
                if not marriage_certificate_no:
                    raise forms.ValidationError({
                        'marriage_certificate_no':
                        'You wrote subject is NOT a citizen and has marriage '
                        'certificate. Please provide certificate number.'})

    def clean_citizen_is_citizen(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('citizen') == YES:
            if cleaned_data.get('legal_marriage') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'legal_marriage': 'This field is not applicable'})
            elif cleaned_data.get('marriage_certificate') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'marriage_certificate': 'This field is not applicable'})

    def household_info(self):
        household_member = self.cleaned_data.get('household_member')
        if household_member:
            if (household_member.relation == HEAD_OF_HOUSEHOLD):
                try:
                    HouseholdInfo.objects.get(
                        household_structure=household_member.household_structure)
                except HouseholdInfo.DoesNotExist:
                    raise forms.ValidationError(
                        'Complete \'{}\' before consenting head of household'.format(
                            HouseholdInfo._meta.verbose_name))

    @property
    def personal_details_changed(self):
        household_member = self.cleaned_data.get("household_member")
        if household_member.personal_details_changed == YES:
            return True
        return False

    def validate_legal_marriage(self):
        if self.cleaned_data.get("legal_marriage") == NO:
            if not (self.cleaned_data.get("marriage_certificate") in [YES, NO]):
                raise forms.ValidationError({
                    'marriage_certificate': 'This field is required.'})


class SubjectConsentForm(ConsentModelFormMixin, forms.ModelForm):

    form_validator_cls = None

    class Meta:
        model = SubjectConsent
        fields = '__all__'
