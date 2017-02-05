from django import forms

from edc_constants.constants import MALE, FEMALE, DWTA

from ..models import Demographics
from ..constants import MARRIED, ALONE
from .form_mixins import SubjectModelFormMixin


class DemographicsForm(SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.validate_marriage()
        self.m2m_single_selection_if('live_with', [ALONE, DWTA])
        self.validate_other_specify('religion', 'religion_other')
        self.validate_other_specify('ethnic', 'ethnic_other')
        return cleaned_data

    def validate_marriage(self):
        cleaned_data = self.cleaned_data
        # validating if married
        if cleaned_data.get('marital_status') == MARRIED:
            subject_visit = cleaned_data.get('subject_visit')
            gender = subject_visit.household_member.gender
            if gender == FEMALE and cleaned_data.get('husband_wives') is not None:
                raise forms.ValidationError(
                    {'husband_wives':
                     'This field is not required for female'})
            elif gender == MALE and cleaned_data.get('num_wives') is not None:
                raise forms.ValidationError(
                    {'num_wives':
                     'This field is not required for male'})
            elif cleaned_data.get('num_wives') is None and gender == FEMALE:
                raise forms.ValidationError(
                    {'num_wives':
                     'Expected a number greater than 0.'})
            elif cleaned_data.get('husband_wives') is None and gender == MALE:
                raise forms.ValidationError(
                    {'husband_wives':
                     'Expected a number greater than 0.'})
            elif gender == FEMALE and cleaned_data.get('num_wives') <= 0:
                raise forms.ValidationError(
                    {'num_wives':
                     'Expected a number greater than 0.'})
            elif gender == MALE and cleaned_data.get('husband_wives') <= 0:
                raise forms.ValidationError(
                    {'husband_wives':
                     'Expected a number greater than 0.'})
        elif cleaned_data.get('marital_status') != MARRIED:
            if cleaned_data.get('num_wives') is not None:
                raise forms.ValidationError({
                    'num_wives':
                    'This field is not required'})
            elif cleaned_data.get('husband_wives') is not None:
                raise forms.ValidationError({
                    'husband_wives':
                    'This field is not required'})

        return cleaned_data

    class Meta:
        model = Demographics
        fields = '__all__'
