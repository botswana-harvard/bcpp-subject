from django import forms

from edc_base.model.constants import DEFAULT_BASE_FIELDS
from edc_constants.choices import YES_NO

from ..choices import MEDICATIONS_TAKEN, HEALTH_CARE_FACILITY
from ..models import HypertensionCardiovascular

from .form_mixins import SubjectModelFormMixin


class HypertensionCardiovascularForm(SubjectModelFormMixin):

    hypertension_diagnosis = forms.ChoiceField(
        choices=YES_NO,
        label='Have you ever been diagnosed with hypertension?',
        required=False,
        widget=forms.RadioSelect())

    medications_taken = forms.MultipleChoiceField(
        choices=MEDICATIONS_TAKEN,
        label='Have you ever taken any of these medications? \
        Tick all that apply',
        required=False,
        widget=forms.CheckboxSelectMultiple())

    health_care_facility = forms.ChoiceField(
        choices=HEALTH_CARE_FACILITY,
        label='If yes: Health facility providing care',
        required=False,
        widget=forms.RadioSelect())

    salt_intake_counselling = forms.ChoiceField(
        choices=YES_NO,
        label='Have you ever been counselled about salt intake \
        by a health care worker in the past 3 years?',
        required=False,
        widget=forms.RadioSelect())

    tobacco_smoking = forms.ChoiceField(
        choices=YES_NO,
        label='Have you ever smoked tobacco products?',
        required=False,
        widget=forms.RadioSelect())

    tobacco_counselling = forms.ChoiceField(
        choices=YES_NO,
        label='If yes to any prior smoking of tobacco products, \
        have you been counselled about smoking cessation / not \
        taking up smoking by a healthcare worker in the past 3 years?',
        required=False,
        widget=forms.RadioSelect())

    physical_activity_counselling = forms.ChoiceField(
        choices=YES_NO,
        label='Have you ever been counselled about the amount of \
        physical activity (or exercise) to maintain by a healthcare \
        worker in the past 3 years?',
        required=False,
        widget=forms.RadioSelect())

    alcohol_counselling = forms.ChoiceField(
        choices=YES_NO,
        label='Have you ever been counselled about correct alcohol \
        intake by a healthcare worker in the past 3 years?',
        required=False,
        widget=forms.RadioSelect())

    weight_counselling = forms.ChoiceField(
        choices=YES_NO,
        label='Have you ever been counselled about what weight you \
        should aim for by a health care worker in the past 3 years?',
        required=False,
        widget=forms.RadioSelect())

    blood_test_for_cholesterol = forms.ChoiceField(
        choices=YES_NO,
        label='Have you ever had a blood test for high cholesterol \
        in the past 3 years?',
        required=False,
        widget=forms.RadioSelect())

    blood_test_for_diabetes = forms.ChoiceField(
        choices=YES_NO,
        label='Have you ever had blood test for sugar diabetes in the \
        past 3 years?',
        required=False,
        widget=forms.RadioSelect())

    medication_still_given = forms.MultipleChoiceField(
        choices=MEDICATIONS_TAKEN,
        label='If yes: Are you still being given this \
        medication (respond for each one ticked)',
        required=False,
        widget=forms.CheckboxSelectMultiple())

    def clean(self):
        self.validate_may_take_blood_pressure()

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
                    return True
            return False

    def validate_may_take_blood_pressure(self):

        if self.cleaned_data['may_take_blood_pressure'] == 'No':
            if self.check_if_questions_are_answered() == True:
                raise forms.ValidationError(
                    'Since the user is not prepared to have weight/bp measured\
                    , nothing else should be filled')

    class Meta:

        model = HypertensionCardiovascular
        fields = '__all__'
