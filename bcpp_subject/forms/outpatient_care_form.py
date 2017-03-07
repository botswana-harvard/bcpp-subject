from django import forms

from edc_constants.constants import MALE, YES

from ..models import OutpatientCare
from .form_mixins import SubjectModelFormMixin


class OutpatientCareForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.subject_visit = cleaned_data.get('subject_visit')

        if cleaned_data.get('govt_health_care'):
            if (cleaned_data.get('govt_health_care') == YES
                    and not cleaned_data.get('care_visits')):
                raise forms.ValidationError({
                    'care_visits':
                    'If participant seeked care from Govt, how many outpatient '
                    'visits were there?'})

            if (cleaned_data.get('govt_health_care') == YES
                    and cleaned_data.get('facility_visited') == 'No visit in past 3 months'):
                raise forms.ValidationError({
                    'facility_visited':
                    'If participant seeked care from Govt, answer about '
                    'facility CANNOT be NO VISIT?'})
            if (cleaned_data.get('govt_health_care') == YES
                    and not cleaned_data.get('care_reason')):
                raise forms.ValidationError({
                    'care_reason':
                    'If participant seeked care from Govt, what was the '
                    'primary reason for seeking care?'})

            if (cleaned_data.get('govt_health_care') == YES
                    and not cleaned_data.get('care_reason')):
                raise forms.ValidationError({
                    'care_reason':
                    'If participant has seeked care, reason for receiving '
                    'CANNOT be NONE?'})
            if (cleaned_data.get('govt_health_care') == YES
                    and str(cleaned_data.get('outpatient_expense')) == 'None'):
                raise forms.ValidationError({
                    'outpatient_expense':
                    'If participant seeked care from Govt, how much did he/she '
                    'have to pay the health care provider?'})
            if (cleaned_data.get('govt_health_care') == YES
                    and not cleaned_data.get('travel_time')):
                raise forms.ValidationError({
                    'travel_time':
                    'how long did it take you to get to the clinic/hospital?'})

            if (cleaned_data.get('govt_health_care') == YES
                    and not cleaned_data.get('waiting_hours')):
                raise forms.ValidationError({
                    'waiting_hours':
                    'If participant has seeked care, waiting hours to be '
                    'seen cannot be None'})

            if (cleaned_data.get('care_reason') == 'Pregnancy'
                    and cleaned_data.get('subject_visit').household_member.gender == MALE):
                raise forms.ValidationError({
                    'care_reason':
                    'If participant is male, pregnancy cannot be choosen'})
            return cleaned_data

    class Meta:
        model = OutpatientCare
        fields = '__all__'
