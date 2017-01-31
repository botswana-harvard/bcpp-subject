import pytz
from copy import deepcopy

from django import forms
from django.conf import settings
from django.forms import ValidationError

from edc_consent.modelform_mixins import ConsentModelFormMixin as BaseConsentModelFormMixin
from edc_constants.constants import NOT_APPLICABLE
from edc_constants.constants import YES, NO

from member.constants import HEAD_OF_HOUSEHOLD
from member.models import HouseholdInfo

from ..models import SubjectConsent

tz = pytz.timezone(settings.TIME_ZONE)


class ConsentModelFormMixin(BaseConsentModelFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        self.clean_consent_with_household_member()
        self.clean_citizen_with_legally_married()
        self.limit_edit_to_current_community()
        self.limit_edit_to_current_survey()
        self.household_info()
        # TODO: does this need to be filled in ??
#         if cleaned_data.get('household_member'):
#             try:
#                 HouseholdHeadEligibility.objects.get(
#                     household_member__in=cleaned_data.get(
#                         'household_member').household_structure.householdmember_set.all())
#             except HouseholdHeadEligibility.DoesNotExist:
#                 raise forms.ValidationError(
#                     'Please fill household head eligibility form before completing subject consent.',
#                     code='invalid')
        return cleaned_data

    def clean_consent_matches_enrollment(self):
        household_member = self.cleaned_data.get("household_member")
        if not SubjectConsent.objects.filter(
                household_member__internal_identifier=household_member.internal_identifier).exclude(
                household_member=household_member).exists():
            consent_datetime = self.cleaned_data.get(
                "consent_datetime", self.instance.consent_datetime)
            options = deepcopy(self.cleaned_data)
            options.update({'consent_datetime': consent_datetime})
            self.instance.matches_enrollment_checklist(
                SubjectConsent(**options), forms.ValidationError)
            self.instance.matches_hic_enrollment(
                SubjectConsent(**options), household_member, forms.ValidationError)

    def clean_consent_with_household_member(self):
        """Validates subject consent values against household member values."""
        initials = self.cleaned_data.get("initials")
        first_name = self.cleaned_data.get("first_name")
        gender = self.cleaned_data.get("gender")
        household_member = self.cleaned_data.get("household_member")
        if household_member:
            if initials != household_member.initials:
                raise forms.ValidationError(
                    'Initials do not match with household member. %(initials)s <> %(hm_initials)s',
                    params={
                        'hm_initials': household_member.initials, 'initials': initials},
                    code='invalid')
            if household_member.first_name != first_name:
                raise forms.ValidationError(
                    'First name does not match with household member. Got %(first_name)s <> %(hm_first_name)s',
                    params={
                        'hm_first_name': household_member.first_name, 'first_name': first_name},
                    code='invalid')
            if household_member.gender != gender:
                raise forms.ValidationError(
                    'Gender does not match with household member. Got %(gender)s <> %(hm_gender)s',
                    params={
                        'hm_gender': household_member.gender, 'gender': gender},
                    code='invalid')

    def clean_citizen_with_legally_married(self):
        citizen = self.cleaned_data.get('citizen')
        legal_marriage = self.cleaned_data.get('legal_marriage')
        marriage_certificate = self.cleaned_data.get('marriage_certificate')
        marriage_certificate_no = self.cleaned_data.get(
            'marriage_certificate_no')
        if citizen == NO:
            if legal_marriage == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You wrote subject is NOT a citizen. Is the subject legally married to a citizen?',
                    code='invalid')
            elif legal_marriage == NO:
                raise forms.ValidationError(
                    'You wrote subject is NOT a citizen and is NOT legally married to a citizen. '
                    'Subject cannot be consented',
                    code='invalid')
            elif legal_marriage == YES and marriage_certificate != YES:
                raise forms.ValidationError(
                    'You wrote subject is NOT a citizen. Subject needs to produce a marriage certificate',
                    code='invalid')
            elif legal_marriage == YES and marriage_certificate == YES:
                if not marriage_certificate_no:
                    raise forms.ValidationError(
                        'You wrote subject is NOT a citizen and has marriage certificate. Please provide certificate number.',
                        code='invalid')

        if citizen == YES:
            if legal_marriage != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You wrote subject is a citizen. That subject is legally married to a citizen is not applicable.',
                    code='invalid')
            elif marriage_certificate != NOT_APPLICABLE:
                raise forms.ValidationError(
                    'You wrote subject is a citizen. The subject\'s marriage certificate is not applicable.',
                    code='invalid')

    def household_info(self):
        household_member = self.cleaned_data.get('household_member')
        if household_member:
            if (household_member.relation == HEAD_OF_HOUSEHOLD):
                try:
                    HouseholdInfo.objects.get(
                        household_structure=household_member.household_structure)
                except HouseholdInfo.DoesNotExist:
                    raise forms.ValidationError(
                        'Complete \'%(model)s\' before consenting head of household',
                        params={'model': HouseholdInfo._meta.verbose_name}, code='invalid')

    @property
    def personal_details_changed(self):
        household_member = self.cleaned_data.get("household_member")
        if household_member.personal_details_changed == YES:
            return True
        return False

    def validate_legal_marriage(self):
        if self.cleaned_data.get("legal_marriage") == NO:
            if not (self.cleaned_data.get("marriage_certificate") in [YES, NO]):
                raise forms.ValidationError(
                    "if married not to a citizen, marriage_certificate proof should be YES or NO.")

    def clean_identity_with_unique_fields(self):
        identity = self.cleaned_data.get('identity')
        first_name = self.cleaned_data.get('first_name')
        initials = self.cleaned_data.get('initials')
        dob = self.cleaned_data.get('dob')
        unique_together_form = self.unique_together_string(
            first_name, initials, dob)
        for consent in self._meta.model.objects.filter(identity=identity):
            unique_together_model = self.unique_together_string(
                consent.first_name, consent.initials, consent.dob)
            if not self.personal_details_changed:
                if unique_together_form != unique_together_model:
                    raise ValidationError(
                        'Identity \'%(identity)s\' is already in use by subject %(subject_identifier)s. '
                        'Please resolve.',
                        params={
                            'subject_identifier': consent.subject_identifier, 'identity': identity},
                        code='invalid')
        for consent in self._meta.model.objects.filter(first_name=first_name, initials=initials, dob=dob):
            if consent.identity != identity:
                raise ValidationError(
                    'Subject\'s identity was previously reported as \'%(existing_identity)s\'. '
                    'You wrote \'%(identity)s\'. Please resolve.',
                    params={
                        'existing_identity': consent.identity, 'identity': identity},
                    code='invalid')


class SubjectConsentForm(ConsentModelFormMixin, forms.ModelForm):

    class Meta:
        model = SubjectConsent
        fields = '__all__'
