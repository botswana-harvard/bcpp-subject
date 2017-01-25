from django import forms

from edc_constants.constants import OTHER

from .form_mixins import SubjectModelFormMixin
from ..models import ImmigrationStatus


class ImmigrationStatusForm (SubjectModelFormMixin):

    def clean(self):

        cleaned_data = super().clean()

        if cleaned_data.get('country_of_origin') == OTHER:
            if cleaned_data.get('country_of_origin_other') == None:
                raise forms.ValidationError({
                    'country_of_origin_other': [
                        'This field is mandatory since other was selected above']})
        else:
            if cleaned_data.get('country_of_origin_other'):
                raise forms.ValidationError({
                    'country_of_origin_other': [
                        'Has to be blank since option is selected']})

        return self.cleaned_data

    class Meta:
        model = ImmigrationStatus
        fields = '__all__'
