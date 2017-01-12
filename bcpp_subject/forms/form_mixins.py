from django import forms

from edc_base.modelform_mixins import CommonCleanModelFormMixin

from ..models import SubjectVisit


class SubjectModelFormMixin(CommonCleanModelFormMixin, forms.ModelForm):

    visit_model = SubjectVisit

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
