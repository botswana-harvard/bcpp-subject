from django import forms

from edc_constants.constants import YES, NO, NEG

from ..exceptions import EnrollmentError
from ..models import HicEnrollment
from ..models import ResidencyMobility
from .form_mixins import SubjectModelFormMixin
from bcpp_subject.models.elisa_hiv_result import ElisaHivResult
from bcpp_subject.models.hiv_result import HivResult
from bcpp_subject.models.subject_visit import SubjectVisit
from bcpp_subject.models.subject_consent import SubjectConsent
from bcpp_subject.models.subject_locator import SubjectLocator

from edc_base.modeladmin_mixins import audit_fields


class AuditFieldsFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in audit_fields:
            self.fields[key].widget.attrs['readonly'] = True


class HicEnrollmentForm (AuditFieldsFormMixin, SubjectModelFormMixin):

    def clean(self):
        cleaned_data = self.cleaned_data

        instance = None
        subject_visit = None
        try:
            subject_visit = SubjectVisit.objects.get(id=self.cleaned_data.get('subject_visit').id)
        except SubjectVisit.DoesNotExist as e:
            raise forms.ValidationError(str(e))
        if self.instance.id:
            instance = self.instance
        else:
            instance = HicEnrollment(**self.cleaned_data)
        if not self.cleaned_data.get('hic_permission', None):
            raise forms.ValidationError('Provide an answer for whether participant gave permission for HIC.')
        if self.cleaned_data.get('hic_permission', None) == YES:
            try:
                instance = self._meta.model(id=self.instance.id, **cleaned_data)
                instance.common_clean()
            except EnrollmentError as e:
                raise forms.ValidationError(str(e))

            # Raise an error if not permanent recident.
            try:
                obj = ResidencyMobility.objects.get(subject_visit=subject_visit)
                if not obj.permanent_resident == YES:
                    raise forms.ValidationError(
                        'Please review \'residency_mobility\' in {} '
                        'form before proceeding with this one.'.format(ResidencyMobility._meta.verbose_name))
            except ResidencyMobility.DoesNotExist:
                raise forms.ValidationError('Please complete {} first.'.format(ResidencyMobility._meta.verbose_name))

            # Raise an error if the intends to relocate.
            try:
                obj = ResidencyMobility.objects.get(subject_visit=subject_visit)
                if not obj.intend_residency == NO:
                    raise forms.ValidationError(
                        'Please review \'intend_residency\' in {} '
                        'form before proceeding with this one.'.format(ResidencyMobility._meta.verbose_name))
            except ResidencyMobility.DoesNotExist:
                raise forms.ValidationError('Please complete {} first.'.format(ResidencyMobility._meta.verbose_name))

            # Raise an error if not NEG.
            try:
                obj = HivResult.objects.get(subject_visit=subject_visit)
                try:
                    elisa_result_obj = ElisaHivResult.objects.get(subject_visit=subject_visit)
                    if (not obj.hiv_result == NEG or not (elisa_result_obj.hiv_result == NEG)):
                        raise forms.ValidationError(
                            'Please review \'hiv_result\' in Today\'s Hiv Result form '
                            'or in Elisa Hiv Result before proceeding with this one.')
                except ElisaHivResult.DoesNotExist:
                    raise forms.ValidationError('Please complete {} first.'.format(ElisaHivResult._meta.verbose_name))
            except HivResult.DoesNotExist:
                raise forms.ValidationError('Please complete {} first.'.format(HivResult._meta.verbose_name))

            # Raise an error if not a citizen or married to a citizen.
            try:
                subject_consent = SubjectConsent.objects.get(household_member=subject_visit.household_member)
                if not ((subject_consent.citizen == YES) or (
                        subject_consent.legal_marriage == YES and
                        subject_consent.marriage_certificate == YES)):
                    raise forms.ValidationError(
                        'Please review \'citizen\', \'legal_marriage\' and '
                        '\'marriage_certificate\' in SubjectConsent for {}. Got {}, {}, {}'.format(
                            subject_consent,
                            subject_consent.citizen,
                            subject_consent.legal_marriage,
                            subject_consent.marriage_certificate))
            except SubjectConsent.DoesNotExist:
                raise forms.ValidationError('Please complete {} first.'.format(SubjectConsent._meta.verbose_name))

            # Raise an error if subject locator is not completed.
            try:
                obj = SubjectLocator.objects.get(subject_identifier=subject_visit.subject_identifier)
                if not (obj.subject_cell or
                        obj.subject_cell_alt or
                        obj.subject_phone or
                        obj.mail_address or
                        obj.physical_address or
                        obj.subject_cell or
                        obj.subject_cell_alt or
                        obj.subject_phone or
                        obj.subject_phone_alt or
                        obj.subject_work_place or
                        obj.subject_work_phone or
                        obj.contact_physical_address or
                        obj.contact_cell or
                        obj.contact_phone):
                    raise forms.ValidationError(
                        'Please review {} to ensure there is some '
                        'way to contact the participant form before proceeding with this one.'.format(
                            SubjectLocator._meta.verbose_name))
            except SubjectLocator.DoesNotExist:
                raise forms.ValidationError('Please complete {} first.'.format(SubjectLocator._meta.verbose_name))

        return super(HicEnrollmentForm, self).clean()

    class Meta:
        model = HicEnrollment
        fields = '__all__'
