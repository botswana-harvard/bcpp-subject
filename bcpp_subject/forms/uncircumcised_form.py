from edc_constants.constants import YES, NOT_APPLICABLE

from ..models import Uncircumcised
from .form_mixins import SubjectModelFormMixin


class UncircumcisedForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.m2m_required_if(
            YES, field='circumcised', m2m_field='health_benefits_smc')
        self.m2m_single_selection_if(
            NOT_APPLICABLE, m2m_field='health_benefits_smc')
        self.validate_other_specify('reason_circ')

        self.applicable_if(YES, 'service_facilities', 'aware_free')

        return cleaned_data

    class Meta:
        model = Uncircumcised
        fields = '__all__'
