from django import forms
from edc_base.modelform_mixins import CommonCleanModelFormMixin, JSONModelFormMixin

from ..models import SubjectVisit


class SubjectModelFormMixin(CommonCleanModelFormMixin, JSONModelFormMixin,
                            forms.ModelForm):

    visit_model = SubjectVisit
    form_validator_cls = None

    def clean(self):
        cleaned_data = super().clean()
        try:
            form_validator = self.form_validator_cls(
                cleaned_data=cleaned_data)
        except TypeError:
            pass
        else:
            cleaned_data = form_validator.validate()
        return cleaned_data
