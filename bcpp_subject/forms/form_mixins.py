from django import forms

from edc_base.modelform_mixins import CommonCleanModelFormMixin
from edc_constants.constants import OTHER

from ..models import SubjectVisit


class SubjectModelFormMixin(CommonCleanModelFormMixin, forms.ModelForm):

    visit_model = SubjectVisit

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def validate_other(self, field, field_other):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get(field)
                and cleaned_data.get(field) == OTHER
                and not cleaned_data.get(field_other)):
            raise forms.ValidationError(
                {field_other:
                 'This field is required.'})
        elif (cleaned_data.get(field)
                and cleaned_data.get(field) != OTHER
                and cleaned_data.get(field_other)):
            raise forms.ValidationError(
                {field_other:
                 'This field is not required.'})
