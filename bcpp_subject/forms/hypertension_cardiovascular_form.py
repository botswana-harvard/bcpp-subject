from django import forms

from edc_constants.constants import NO, NOT_APPLICABLE, OTHER

from ..models import HypertensionCardiovascular

from .form_mixins import SubjectModelFormMixin


class HypertensionCardiovascularForm(SubjectModelFormMixin):

    def clean(self):
        self.validate_hypertension_diagnosis()
        self.validate_if_other_medication_taken()
        self.validate_if_other_medication_still_given()
        return self.cleaned_data

    def validate_hypertension_diagnosis(self):
        cleaned_data = super().clean()
        if cleaned_data.get('may_take_blood_pressure') == NO:
            if cleaned_data.get('hypertension_diagnosis') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'hypertension_diagnosis': [
                        'Not Applicable is the only valid answer']})
        return cleaned_data

    def validate_if_other_medication_taken(self):
        cleaned_data = super().clean()
        if cleaned_data.get('if_other_medications_taken'):
            if not any(medication_list.name == OTHER
                       for medication_list in cleaned_data.get('medications_taken')):
                raise forms.ValidationError({
                    'if_other_medications_taken': [
                        'Cannot fill this field unless Other is selected above']})
        else:
            if any(medication_list.name == OTHER
                   for medication_list in cleaned_data.get('medications_taken')):
                raise forms.ValidationError({
                    'if_other_medications_taken': [
                        'This field is mandatory since other was selected above']})
        return cleaned_data

    def validate_if_other_medication_still_given(self):
        cleaned_data = super().clean()
        if cleaned_data.get('if_other_medication_still_given'):
            if not any(medication_list.name == OTHER
                       for medication_list in cleaned_data.get('medication_still_given')):
                raise forms.ValidationError({
                    'if_other_medication_still_given': [
                        'Cannot fill this field unless Other is selected above']})
        else:
            if any(medication_list.name == OTHER
                   for medication_list in cleaned_data.get('if_other_medication_still_given')):
                raise forms.ValidationError({
                    'if_other_medication_still_given': [
                        'This field is mandatory since other was selected above']})
        return cleaned_data

    class Meta:

        model = HypertensionCardiovascular
        fields = '__all__'
