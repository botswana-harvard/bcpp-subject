from django import forms
from django.utils.translation import gettext_lazy as _

from ..constants import ANNUAL
from ..exceptions import CircumcisionError
from ..models import Circumcision, Uncircumcised, Circumcised

from .form_mixins import SubjectModelFormMixin
from edc_constants.constants import YES


class CircumcisionForm (SubjectModelFormMixin):

    optional_labels = {
        ANNUAL: {'circumcised': (
            'Have you been circumcised since we last spoke with you?'),
        }
    }

    class Meta:
        model = Circumcision
        fields = '__all__'


class CircumcisedForm (SubjectModelFormMixin):

    def clean(self):
        if self.cleaned_data.get('circumcised') == YES and not self.cleaned_data.get('health_benefits_smc'):
            raise forms.ValidationError({'health_benefits_smc': _('Please select all that apply.')})
        return super().clean()

    class Meta:
        model = Circumcised
        fields = '__all__'


class UncircumcisedForm (SubjectModelFormMixin):

    def clean(self):
        if self.cleaned_data.get('circumcised') == YES and not self.cleaned_data.get('health_benefits_smc'):
            raise forms.ValidationError({'health_benefits_smc': _('Please select all that apply.')})
        return super().clean()

    class Meta:
        model = Uncircumcised
        fields = '__all__'
