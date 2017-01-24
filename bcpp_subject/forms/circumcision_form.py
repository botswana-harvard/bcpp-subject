from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import Circumcision, Uncircumcised, Circumcised

from .form_mixins import SubjectModelFormMixin
from edc_constants.constants import YES


class CircumcisionForm (SubjectModelFormMixin):

    class Meta:
        model = Circumcision
        fields = '__all__'


class CircumcisedForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('circumcised') == YES and not cleaned_data.get('health_benefits_smc'):
            raise forms.ValidationError({
                'health_benefits_smc': _('Please select all that apply.')})
        return cleaned_data

    class Meta:
        model = Circumcised
        fields = '__all__'


class UncircumcisedForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('circumcised') == YES and not cleaned_data.get('health_benefits_smc'):
            raise forms.ValidationError({
                'health_benefits_smc': _('Please select all that apply.')})
        return cleaned_data

    class Meta:
        model = Uncircumcised
        fields = '__all__'
