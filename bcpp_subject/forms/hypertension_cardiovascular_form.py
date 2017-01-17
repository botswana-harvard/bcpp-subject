from django import forms

from edc_constants.constants import NO, NOT_APPLICABLE

from ..models import HypertensionCardiovascular

from .form_mixins import SubjectModelFormMixin


class HypertensionCardiovascularForm(SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.validate_hypertension_diagnosis()
        return cleaned_data

    def validate_hypertension_diagnosis(self):

        if self.cleaned_data.get('may_take_blood_pressure') == NO:
            if self.cleaned_data.get('hypertension_diagnosis') != NOT_APPLICABLE:
                raise forms.ValidationError('Not Applicable is the only valid answer')
                raise forms.ValidationError({
                    'hypertension_diagnosis': _('Not Applicable is the only valid answer')})

    class Meta:

        model = HypertensionCardiovascular
        fields = '__all__'
