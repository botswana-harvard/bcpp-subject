from django import forms

from edc_base.model.constants import DEFAULT_BASE_FIELDS

from ..choices import MEDICATIONS_TAKEN
from ..models import HypertensionCardiovascular

from .form_mixins import SubjectModelFormMixin


class HypertensionCardiovascularForm(SubjectModelFormMixin):

    medications_taken = forms.MultipleChoiceField(
        choices=MEDICATIONS_TAKEN,
        label='Have you ever taken any of these medications? \
        Tick all that apply',
        widget=forms.CheckboxSelectMultiple())

    is_medication_still_given = forms.MultipleChoiceField(
        choices=MEDICATIONS_TAKEN,
        label='If yes: Are you still being given this \
        medication (respond for each one ticked)',
        widget=forms.CheckboxSelectMultiple())

    def get_field_data_as_list(self):
        field_list = []
        for field in HypertensionCardiovascular._meta.fields:
            if field.name not in ['may_take_blood_pressure'] + DEFAULT_BASE_FIELDS:
                field_list.append(self.cleaned_data[field])
            return field_list

    def check_if_questions_are_answered(self):
            field_data = self.get_field_data_as_list()
            for _field_data in field_data:
                if _field_data:
                    return False
            return True

    def validate_may_take_blood_pressure(self):

        if self.cleaned_data['may_take_blood_pressure'] == 'No':
            if self.check_if_questions_are_answered() == True:
                raise forms.ValidationError(
                    'How many hours did it take you to get to the hospital?')

    class Meta:

        model = HypertensionCardiovascular

        fields = '__all__'
