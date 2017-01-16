from django import forms

from ..models import HypertensionCardiovascular

from .form_mixins import SubjectModelFormMixin
from edc_constants.constants import NO


class HypertensionCardiovascularForm(SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        # self.validate_may_take_blood_pressure()
        return cleaned_data

    def validate_may_take_blood_pressure(self):
        # FIXME: 
        if self.cleaned_data.get('may_take_blood_pressure') == NO:
                raise forms.ValidationError(
                    'Since the user is not prepared to have weight/bp measured\
                    , nothing else should be filled')

    class Meta:

        model = HypertensionCardiovascular
        fields = '__all__'
