from django import forms

from edc_constants.constants import YES, NOT_APPLICABLE, DWTA, NOT_SURE

from ..models import Circumcision, Uncircumcised, Circumcised
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


class CircumcisedForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.m2m_required_if(YES, 'circumcised', 'health_benefits_smc')
        self.m2m_single_selection_if('health_benefits_smc', [DWTA, NOT_SURE])
        self.validate_other_specify('reason_circ')
        self.validate_other_specify('why_circ')
        return cleaned_data

    class Meta:
        model = Circumcised
        fields = '__all__'


class UncircumcisedForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.m2m_required_if(YES, 'circumcised', 'health_benefits_smc')
        self.m2m_single_selection_if('health_benefits_smc', [NOT_APPLICABLE])
        self.validate_other_specify('reason_circ')

        self.applicable_if(YES, 'service_facilities', 'aware_free')

        return cleaned_data

    class Meta:
        model = Uncircumcised
        fields = '__all__'
