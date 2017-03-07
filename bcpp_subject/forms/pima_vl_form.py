from django import forms

from edc_constants.constants import YES, NO

from ..models import PimaVl
from .form_mixins import SubjectModelFormMixin


class PimaVlForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(PimaVlForm, self).clean()

        if cleaned_data.get('poc_vl_today') == NO:
            if not cleaned_data.get('poc_vl_today_other'):
                raise forms.ValidationError(
                    'If POC VL NOT done today, please explain why not?')
            if cleaned_data.get('pima_id'):
                raise forms.ValidationError(
                    'Do not provide the PIMA machine id if the POC VL was not performed')
            if cleaned_data.get('poc_vl_value'):
                raise forms.ValidationError(
                    'POC VL was not performed, do not provide the POC viral load count')

        if cleaned_data.get('poc_vl_today') == YES:
            if not cleaned_data.get('pima_id'):
                raise forms.ValidationError(
                    'If POC VL done today, please provide machine id?')
            if not cleaned_data.get('poc_vl_value'):
                raise forms.ValidationError(
                    'If POC VL done today, what is the POC viral load count?')
            if not cleaned_data.get('time_of_test') or not cleaned_data.get('time_of_result'):
                raise forms.ValidationError(
                    'Time of test and time of result should be provided.')

    def validate_poc_vl_today_no(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('poc_vl_today') == NO:
            if not cleaned_data.get('poc_vl_today_other'):
                raise forms.ValidationError(
                    'If POC VL NOT done today, please explain why not?')
            if cleaned_data.get('pima_id'):
                raise forms.ValidationError(
                    'Do not provide the PIMA machine id if the POC VL was not performed')
            if cleaned_data.get('poc_vl_value'):
                raise forms.ValidationError(
                    'POC VL was not performed, do not provide the POC viral load count')

    class Meta:
        model = PimaVl
        fields = '__all__'
