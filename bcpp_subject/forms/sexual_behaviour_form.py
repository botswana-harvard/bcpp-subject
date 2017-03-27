from django import forms

from edc_constants.constants import YES, NO, DWTA

from ..models import SexualBehaviour
from .form_mixins import SubjectModelFormMixin
from bcpp_subject.forms.form_mixins import PreviousAppointmentFormMixin


class SexualBehaviourForm (PreviousAppointmentFormMixin, SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.not_required_if(
            NO, DWTA, field='ever_sex',
            field_required='lifetime_sex_partners',
            optional_if_dwta=True)
        self.not_required_if(
            NO, DWTA, field='ever_sex',
            field_required='last_year_partners',
            optional_if_dwta=True)
        if (cleaned_data.get('last_year_partners')
                and cleaned_data.get('lifetime_sex_partners')
                and int(cleaned_data.get('last_year_partners'))
                > int(cleaned_data.get('lifetime_sex_partners'))):
            raise forms.ValidationError({
                'last_year_partners':
                'Cannot exceed {} partners from above.'.format(
                    cleaned_data.get('lifetime_sex_partners'))})

        if cleaned_data.get('last_year_partners'):
            self.required_if_true(
                int(cleaned_data.get('last_year_partners')) > 0,
                field_required='more_sex')

        self.not_required_if(
            NO, DWTA, field='ever_sex',
            field_required='first_sex',
            optional_if_dwta=True)
        self.validate_first_sex_age()
        self.applicable_if(
            YES, field='ever_sex', field_applicable='first_sex_partner_age')
        self.validate_other_specify(
            'first_sex_partner_age', other_stored_value='gte_19')
        self.not_required_if(
            NO, DWTA, field='ever_sex',
            field_required='condom',
            optional_if_dwta=True)
        self.not_required_if(
            NO, DWTA, field='ever_sex',
            field_required='alcohol_sex',
            optional_if_dwta=True)
        return cleaned_data

    def validate_first_sex_age(self):
        cleaned_data = self.cleaned_data
        age_in_years = cleaned_data.get(
            'subject_visit').household_member.age_in_years
        if (cleaned_data.get('first_sex') and age_in_years
                and (int(age_in_years) < int(cleaned_data.get('first_sex')))):
            raise forms.ValidationError({
                'first_sex': 'Invalid. Participant is {} years old.'.format(
                    age_in_years)})

    class Meta:
        model = SexualBehaviour
        fields = '__all__'
