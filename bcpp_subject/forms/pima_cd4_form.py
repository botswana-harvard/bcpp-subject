from django import forms

from ..models import PimaCd4
from .form_mixins import SubjectModelFormMixin, MobileTestModelFormMixin


class PimaCd4Form (MobileTestModelFormMixin, SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        if (cleaned_data.get('result_value')
                and cleaned_data.get('result_value') > 3000):
            forms.ValidationError({
                'result_value': 'Invalid result value.'})
        return cleaned_data

    class Meta:
        model = PimaCd4
        fields = '__all__'
