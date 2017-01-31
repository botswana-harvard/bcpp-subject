from django import forms

from edc_base.utils import age
from edc_constants.constants import YES, NO, NEG

from ..models import (
    HicEnrollment, ElisaHivResult, HivResult, SubjectConsent,
    SubjectLocator, ResidencyMobility)

from .form_mixins import SubjectModelFormMixin


class HicEnrollmentForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = self.cleaned_data

        try:
            subject_consent = SubjectConsent.objects.get(
                subject_identifier=cleaned_data.get(
                    'subject_visit').subject_identifier)
        except SubjectConsent.DoesNotExist:
            raise forms.ValidationError(
                'Please complete {} first.'.format(
                    SubjectConsent._meta.verbose_name))

        try:
            subject_locator = SubjectLocator.objects.get(
                subject_identifier=cleaned_data.get(
                    'subject_visit').subject_identifier)
        except SubjectLocator.DoesNotExist:
            raise forms.ValidationError(
                'Please complete {} first.'.format(
                    SubjectLocator._meta.verbose_name))

        if self.cleaned_data.get('hic_permission') == NO:
            raise forms.ValidationError(
                {'hic_permission': 'Subject is not eligible'})
        elif self.cleaned_data.get('hic_permission') == YES:
            consent_age = age(
                subject_consent.dob, subject_consent.consent_datetime)
            if not 16 <= consent_age.years <= 64:
                raise forms.ValidationError(
                    'Invalid age. Got {}'.format(consent_age.years))

            # Raise an error if not permanent recident.
            try:
                obj = ResidencyMobility.objects.get(
                    subject_visit=cleaned_data.get('subject_visit'))
            except ResidencyMobility.DoesNotExist:
                raise forms.ValidationError(
                    'Please complete {} first.'.format(
                        ResidencyMobility._meta.verbose_name))
            else:
                if not obj.permanent_resident == YES:
                    raise forms.ValidationError(
                        'Please review \'residency_mobility\' on {} '
                        'before proceeding.'.format(
                            ResidencyMobility._meta.verbose_name))
            # Raise an error if the intends to relocate.
            try:
                obj = ResidencyMobility.objects.get(
                    subject_visit=cleaned_data.get('subject_visit'))
            except ResidencyMobility.DoesNotExist:
                raise forms.ValidationError(
                    'Please complete {} first.'.format(
                        ResidencyMobility._meta.verbose_name))
            else:
                if not obj.intend_residency == NO:
                    raise forms.ValidationError(
                        'Please review \'intend_residency\' on {} '
                        'before proceeding.'.format(
                            ResidencyMobility._meta.verbose_name))
            # Raise an error if not NEG.
            try:
                obj = HivResult.objects.get(
                    subject_visit=cleaned_data.get('subject_visit'))
            except HivResult.DoesNotExist:
                raise forms.ValidationError(
                    'Please complete {} first.'.format(
                        HivResult._meta.verbose_name))
            else:
                try:
                    elisa_result_obj = ElisaHivResult.objects.get(
                        subject_visit=cleaned_data.get('subject_visit'))
                except ElisaHivResult.DoesNotExist:
                    raise forms.ValidationError(
                        'Please complete {} first.'.format(
                            ElisaHivResult._meta.verbose_name))
                else:
                    if (not obj.hiv_result == NEG
                            or not (elisa_result_obj.hiv_result == NEG)):
                        raise forms.ValidationError(
                            'Please review \'hiv_result\' in Today\'s Hiv '
                            'Result form or in Elisa Hiv Result before '
                            'proceeding.')

            # Raise an error if not a citizen or married to a citizen.
            if not ((subject_consent.citizen == YES) or (
                    subject_consent.legal_marriage == YES and
                    subject_consent.marriage_certificate == YES)):
                raise forms.ValidationError(
                    'Please review \'citizen\', \'legal_marriage\' and '
                    '\'marriage_certificate\' in SubjectConsent for {}. '
                    'Got {}, {}, {}'.format(
                        subject_consent,
                        subject_consent.citizen,
                        subject_consent.legal_marriage,
                        subject_consent.marriage_certificate))

            # Raise an error if subject locator is not completed.
            if not (subject_locator.subject_cell or
                    subject_locator.subject_cell_alt or
                    subject_locator.subject_phone or
                    subject_locator.mail_address or
                    subject_locator.physical_address or
                    subject_locator.subject_cell or
                    subject_locator.subject_cell_alt or
                    subject_locator.subject_phone or
                    subject_locator.subject_phone_alt or
                    subject_locator.subject_work_place or
                    subject_locator.subject_work_phone or
                    subject_locator.contact_physical_address or
                    subject_locator.contact_cell or
                    subject_locator.contact_phone):
                raise forms.ValidationError(
                    'Please review {} to ensure there is some '
                    'way to contact the participant form before '
                    'proceeding.'.format(
                        SubjectLocator._meta.verbose_name))

        return super(HicEnrollmentForm, self).clean()

    class Meta:
        model = HicEnrollment
        fields = '__all__'
