from django import forms

from edc_base.model.constants import DEFAULT_BASE_FIELDS
from edc_constants.constants import NO

from ..models import HypertensionCardiovascular

from .form_mixins import SubjectModelFormMixin


class HypertensionCardiovascularForm(SubjectModelFormMixin):

    def clean(self):
        self.validate_tobacco_smoking()
        self.validate_not_available_fields()
        self.validate_if_medication_taken_other()
        self.validate_if_other_medication_still_given()
        self.validate_blank_fields()
        return self.cleaned_data

    def validate_if_medication_taken_other(self):
        cleaned_data = super().clean()
        if cleaned_data.get('medication_taken_other'):
            if not any(medication_list.name == OTHER
                       for medication_list in cleaned_data.get('medication_taken')):
                raise forms.ValidationError({
                    'medication_taken_other': [
                        'Cannot fill this field unless Other is ',
                        'selected above']})
        else:
            if any(medication_list.name == OTHER
                   for medication_list in cleaned_data.get('medication_taken')):
                raise forms.ValidationError({
                    'medication_taken_other': [
                        'This field is mandatory since other was '
                        'selected above']})
        return cleaned_data

    def validate_if_other_medication_still_given(self):
        cleaned_data = super().clean()
        if cleaned_data.get('medication_given_other'):
            if not any(medication_list.name == OTHER
                       for medication_list in cleaned_data.get('medication_given')):
                raise forms.ValidationError({
                    'medication_given_other': [
                        'Cannot fill this field unless Other is '
                        'selected above']})
        else:
            if any(medication_list.name == OTHER
                   for medication_list in cleaned_data.get('medication_given')):
                raise forms.ValidationError({
                    'medication_given_other': [
                        'This field is mandatory since other was '
                        'selected above']})
        return cleaned_data

    def validate_blank_fields(self):
        cleaned_data = super().clean()

        blank_fields = ['right_arm_one',
                        'left_arm_one',
                        'right_arm_two',
                        'left_arm_two',
                        'waist_reading_one',
                        'waist_reading_two',
                        'hip_reading_one',
                        'hip_reading_two']

        if cleaned_data.get('may_take_blood_pressure') == NO:
            for field in blank_fields:
                if cleaned_data.get(field):
                    raise forms.ValidationError({
                        field: [
                            'This field should be left empty as the '
                            'participant does not agree to have their blood '
                            'pressure and waist/hip measured.']})

    def validate_not_available_fields(self):
        cleaned_data = super().clean()
        all_na_fields = []
        fields_to_exclude = DEFAULT_BASE_FIELDS + ['may_take_blood_pressure',
                                                   'subject_visit',
                                                   'report_datetime',
                                                   'medication_taken',
                                                   'medication_given',
                                                   'consent_version',
                                                   'medication_taken_other',
                                                   'medication_given_other',
                                                   'right_arm_one',
                                                   'left_arm_one',
                                                   'right_arm_two',
                                                   'left_arm_two',
                                                   'waist_reading_one',
                                                   'waist_reading_two',
                                                   'hip_reading_one',
                                                   'hip_reading_two']

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

    def validate_tobacco_smoking(self):
        cleaned_data = super().clean()

        if cleaned_data.get('tobacco_smoking') == 'never':
            if cleaned_data.get('tobacco_counselling') != 'N/A':
                raise forms.ValidationError({
                    'tobacco_counselling': [
                        'Not Applicable is the only valid answer']})
        return cleaned_data

    class Meta:

        model = HypertensionCardiovascular
        fields = '__all__'
