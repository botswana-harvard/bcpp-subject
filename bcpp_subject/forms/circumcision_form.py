from django import forms

from edc_constants.constants import YES, NOT_APPLICABLE

from ..models import Circumcision
from .form_mixins import SubjectModelFormMixin


class CircumcisionForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        if (cleaned_data.get('circumcised') == YES
                and cleaned_data.get('circumcised_location') == NOT_APPLICABLE):
            raise forms.ValidationError({
                'circumcised_location':
                'This field is applicable'})
        elif (cleaned_data.get('circumcised') != YES
              and cleaned_data.get('circumcised_location') != NOT_APPLICABLE):
            raise forms.ValidationError({
                'circumcised_location':
                'This field is not applicable'})
        self.validate_other_specify('circumcised_location')
        return cleaned_data

    class Meta:
        model = Circumcision
        fields = '__all__'
