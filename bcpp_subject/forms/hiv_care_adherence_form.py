from datetime import date

from django import forms

from edc_constants.constants import YES, NO, OTHER

from ..models import HivCareAdherence

from .form_mixins import SubjectModelFormMixin


class HivCareAdherenceForm(SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.validate_ever_taken_arv()

        if cleaned_data.get('ever_taken_arv') == NO:
            if cleaned_data.get('arv_stop'):
                raise forms.ValidationError({
                    'arv_stop':
                    'Participant has never taken ART. This field is not required.'})
            if cleaned_data.get('on_arv') == YES:
                raise forms.ValidationError({
                    'on_arv':
                    'Participant has never taken ART. This field is not required.'})

        self.validate_on_arv()
        self.validate_not_on_arv()

        if (cleaned_data.get('medical_care') == NO
                and not cleaned_data.get('no_medical_care')):
            raise forms.ValidationError(
                {'no_medical_care':
                 ('If participant has not received any medical care, '
                  'please give reason why not')})
        if (cleaned_data.get('ever_recommended_arv') == YES
                and cleaned_data.get('ever_taken_arv') == NO
                and not cleaned_data.get('why_no_arv')):
            raise forms.ValidationError({
                'why_no_arv':
                ('If participant has not taken any ARV\'s, '
                 'give the main reason why not')})
        if (cleaned_data.get('arv_stop') == OTHER
                and not cleaned_data.get('arv_stop_other')):
            raise forms.ValidationError({
                'arv_stop_other':
                'If participant reason for stopping ARV\'s is \'OTHER\', '
                'specify reason why stopped taking ARV\'s?'})
        if cleaned_data.get('first_positive'):
            if cleaned_data.get('first_positive') == date.today():
                raise forms.ValidationError({
                    'first_positive':
                    'Date first received HIV positive result CANNOT be '
                    'today. Please correct.'})
        if cleaned_data.get('next_appointment_date'):
            if not cleaned_data.get('next_appointment_date') >= date.today():
                raise forms.ValidationError({
                    'next_appointment_date':
                    'The next appointment date must be on or '
                    'after the report datetime. You entered '
                    '{0}'.format(cleaned_data.get(
                        'next_appointment_date').strftime('%Y-%m-%d'))})

        return cleaned_data

    def validate_ever_taken_arv(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('ever_taken_arv') == YES:
            if (cleaned_data.get('on_arv') == NO
                    and not cleaned_data.get('arv_stop_date')):
                raise forms.ValidationError({
                    'arv_stop_date':
                    'Participant has taken ART but stopped. This field is required.'})
            if not cleaned_data.get('first_arv'):
                raise forms.ValidationError({
                    'first_arv':
                    'Participant has taken ART. This field is required.'})
            if cleaned_data.get('why_no_arv'):
                raise forms.ValidationError({
                    'why_no_arv':
                    'Participant has taken ART. This field is not required.'})

    def validate_on_arv(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('on_arv') == YES:
            if not cleaned_data.get('adherence_4_day'):
                raise forms.ValidationError({
                    'adherence_4_day':
                    'Participant is on ART. This field is required'})
            if not cleaned_data.get('clinic_receiving_from'):
                raise forms.ValidationError({
                    'clinic_receiving_from':
                    'Participant is on ART. This field is required'})
            if not cleaned_data.get('next_appointment_date'):
                raise forms.ValidationError({
                    'next_appointment_date':
                    'Participant is on ART. This field is required'})
            if cleaned_data.get('arv_stop_date'):
                raise forms.ValidationError({
                    'arv_stop_date':
                    'Participant is on ART. This field is not required'})
            if cleaned_data.get('arv_stop'):
                raise forms.ValidationError({
                    'arv_stop':
                    'Participant is on ART. This field is not required'})
            if not cleaned_data.get('arv_evidence'):
                raise forms.ValidationError({
                    'arv_evidence':
                    'Participant is on ART. This field is required'})

    def validate_not_on_arv(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('on_arv') == NO:
            if cleaned_data.get('adherence_4_wk'):
                raise forms.ValidationError({
                    'adherence_4_wk':
                    'Participant is not on ART. This field is not required'})
            if cleaned_data.get('adherence_4_day'):
                raise forms.ValidationError({
                    'adherence_4_day':
                    'Participant is not on ART. This field is not required'})
            if cleaned_data.get('clinic_receiving_from'):
                raise forms.ValidationError({
                    'clinic_receiving_from':
                    'Participant is not on ART. This field is not required'})
            if cleaned_data.get('next_appointment_date'):
                raise forms.ValidationError({
                    'next_appointment_date':
                    'Participant is not on ART. This field is not required'})
            if cleaned_data.get('arv_stop_date'):
                raise forms.ValidationError({
                    'arv_stop_date':
                    'Participant is not on ART. This field is not required'})
            if cleaned_data.get('arv_stop_other'):
                raise forms.ValidationError({
                    'arv_stop_other':
                    'Participant is not on ART. This field is not required'})
            if cleaned_data.get('arv_stop'):
                raise forms.ValidationError({
                    'arv_stop':
                    'Participant is not on ART. This field is not required'})

    class Meta:
        model = HivCareAdherence
        fields = '__all__'
