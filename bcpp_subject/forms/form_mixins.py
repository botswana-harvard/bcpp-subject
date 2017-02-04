from django import forms

from edc_base.modelform_mixins import (
    CommonCleanModelFormMixin, OtherSpecifyValidationMixin,
    ApplicableValidationMixin, Many2ManyModelValidationMixin)

from ..models import SubjectVisit


class SubjectModelFormMixin(CommonCleanModelFormMixin,
                            OtherSpecifyValidationMixin,
                            ApplicableValidationMixin,
                            Many2ManyModelValidationMixin,
                            forms.ModelForm):

    visit_model = SubjectVisit

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
