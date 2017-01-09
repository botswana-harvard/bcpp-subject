from django import forms

from edc_constants.constants import YES, NO

from ..models import HivLinkageToCare, HivCareAdherence

from .form_mixins import SubjectModelFormMixin


class HivLinkageToCareForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(HivLinkageToCareForm, self).clean()
        try:
            hiv_care_adherence = HivCareAdherence.objects.get(
                subject_visit=cleaned_data.get('subject_visit'))
        except HivCareAdherence.DoesNotExist:
            raise forms.ValidationError(
                'Please complete {} first.'.format(HivCareAdherence._meta.verbose_name))
        else:
            if hiv_care_adherence.on_arv == YES and cleaned_data.get('startered_therapy', None) == NO:
                raise forms.ValidationError(
                    {'startered_therapy': 'If participant is said to be on ART on the {} '
                        'this is contrary to the information given on question 12'.format(
                            HivCareAdherence._meta.verbose_name)})
            if hiv_care_adherence.on_arv == NO and cleaned_data.get('startered_therapy', None) == YES:
                raise forms.ValidationError(
                    {'startered_therapy': 'If participant is said to be not on art on the '
                        ' {} this is contrary to the information given on question 12'.format(
                            HivCareAdherence._meta.verbose_name)})
        return cleaned_data

    class Meta:
        model = HivLinkageToCare
        fields = '__all__'
