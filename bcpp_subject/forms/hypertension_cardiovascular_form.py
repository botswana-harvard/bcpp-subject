from django import forms

from edc_base.model.constants import DEFAULT_BASE_FIELDS
from edc_constants.constants import NO, OTHER

from ..models import HypertensionCardiovascular

from .form_mixins import SubjectModelFormMixin


class HypertensionCardiovascularForm(SubjectModelFormMixin):

    def clean(self):
        self.validate_not_available_fields()
        self.validate_if_other_medication_taken()
        self.validate_if_other_medication_still_given()
        return self.cleaned_data

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

    def validate_not_available_fields(self):
        cleaned_data = super().clean()
        all_na_fields = []
        fields_to_exclude = DEFAULT_BASE_FIELDS + ['may_take_blood_pressure',
                                                   'subject_visit',
                                                   'waistcircumferencemeasurement',
                                                   'report_datetime',
                                                   'bpmeasurement',
                                                   'medications_taken',
                                                   'medication_still_given',
                                                   'consent_version',
                                                   'if_other_medications_taken',
                                                   'if_other_medication_still_given']

        for field in HypertensionCardiovascular._meta.get_fields():
            if field.name not in fields_to_exclude:
                all_na_fields.append(field.name)

        if cleaned_data.get('may_take_blood_pressure') == NO:
            for field in all_na_fields:
                if cleaned_data.get(field) != 'N/A':
                    raise forms.ValidationError({
                        field: [
                            'Not Applicable is the only valid answer']})
        return cleaned_data

    class Meta:

        model = HypertensionCardiovascular
        fields = '__all__'
