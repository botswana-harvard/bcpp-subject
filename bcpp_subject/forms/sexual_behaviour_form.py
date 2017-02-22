from django import forms

from edc_constants.constants import YES, DWTA, NO

from ..models import SexualBehaviour
from .form_mixins import SubjectModelFormMixin
from bcpp_subject.forms.form_mixins import PreviousAppointmentFormMixin


class SexualBehaviourForm (PreviousAppointmentFormMixin, SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.validate_with_previous_instance()
        self.not_required_if(
            NO, DWTA, field='ever_sex', field_required='lifetime_sex_partners')
        self.not_required_if(
            NO, DWTA, field='ever_sex', field_required='last_year_partners')

        if (cleaned_data.get('last_year_partners')
                and cleaned_data.get('lifetime_sex_partners')
                and cleaned_data.get('last_year_partners')
                > cleaned_data.get('lifetime_sex_partners')):
            raise forms.ValidationError({
                'last_year_partners':
                'Cannot exceed {} partners from above.'.format(
                    cleaned_data.get('lifetime_sex_partners'))})

        if cleaned_data.get('last_year_partners'):
            self.required_if_true(
                int(cleaned_data.get('last_year_partners')) > 0,
                field_required='more_sex')

        self.required_if(YES, field='ever_sex', field_required='first_sex')
        self.validate_first_sex_age()
        self.applicable_if(
            YES, field='ever_sex', field_applicable='first_sex_partner_age')
        self.validate_other_specify(
            'first_sex_partner_age', other_stored_value='gte_19')
        self.required_if(YES, field='ever_sex', field_required='condom')
        self.required_if(YES, field='ever_sex', field_required='alcohol_sex')
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

    def validate_with_previous_instance(self):
        cleaned_data = self.cleaned_data
        try:
            SexualBehaviour.objects.get(
                subject_visit__appointment=self.previous_appointment,
                ever_sex=YES)
        except SexualBehaviour.DoesNotExist:
            pass
        else:
            if cleaned_data.get('ever_sex') != YES:
                raise forms.ValidationError({
                    'ever_sex':
                    'Expected \'Yes\' as previously reported on {}.'.format(
                        self.previous_appointment_rdate.date().strftime(
                            '%Y-%m-%d'))})

    class Meta:
        model = SexualBehaviour
        fields = '__all__'
