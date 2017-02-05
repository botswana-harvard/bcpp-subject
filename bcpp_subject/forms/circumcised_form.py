from edc_constants.constants import YES, DWTA, NOT_SURE

from ..models import Circumcised
from .form_mixins import SubjectModelFormMixin


class CircumcisedForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.m2m_required_if(
            YES, field='circumcised', m2m_field='health_benefits_smc')
        self.m2m_single_selection_if(
            DWTA, NOT_SURE, m2m_field='health_benefits_smc')
        self.validate_other_specify('reason_circ')
        self.validate_other_specify('why_circ')
        return cleaned_data

    class Meta:
        model = Circumcised
        fields = '__all__'
