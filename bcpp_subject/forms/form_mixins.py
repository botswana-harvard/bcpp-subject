from django import forms

from edc_base.modelform_mixins import (
    CommonCleanModelFormMixin, OtherSpecifyValidationMixin)

from ..models import SubjectVisit


class SubjectModelFormMixin(CommonCleanModelFormMixin,
                            OtherSpecifyValidationMixin,
                            forms.ModelForm):

    visit_model = SubjectVisit

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
