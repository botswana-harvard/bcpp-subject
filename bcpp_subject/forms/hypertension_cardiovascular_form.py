from django import forms

from edc_base.model.constants import DEFAULT_BASE_FIELDS
from edc_constants.constants import NO, NEVER, YES

from ..models import HypertensionCardiovascular

from .form_mixins import SubjectModelFormMixin


class HypertensionCardiovascularForm(SubjectModelFormMixin):

    def clean(self):

        self.applicable_if(
            YES, field='tobacco_smoking',
            field_applicable='tobacco_current')
        self.applicable_if(
            YES, field='tobacco_smoking',
            field_applicable='tobacco_counselling')

        self.m2m_other_specify_applicable()('medication_taken')
        self.m2m_other_specify_applicable()('medication_taken')

        self.required_if(YES, 'may_take_blood_pressure', 'right_arm_one')
        self.required_if(YES, 'may_take_blood_pressure', 'left_arm_one')
        self.required_if(YES, 'may_take_blood_pressure', 'right_arm_two')
        self.required_if(YES, 'may_take_blood_pressure', 'left_arm_two')
        self.required_if(YES, 'may_take_blood_pressure', 'waist_reading_one')
        self.required_if(YES, 'may_take_blood_pressure', 'waist_reading_two')
        self.required_if(YES, 'may_take_blood_pressure', 'hip_reading_one')
        self.required_if(YES, 'may_take_blood_pressure', 'hip_reading_two')
        self.validate_not_available_fields()
        return self.cleaned_data

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
