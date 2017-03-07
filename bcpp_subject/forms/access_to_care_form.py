from ..models import AccessToCare

from .form_mixins import SubjectModelFormMixin
from edc_constants.constants import DWTA, OTHER


class AccessToCareForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.validate_other_specify('access_care')
        self.m2m_single_selection_if(
            DWTA, m2m_field='medical_care_access')
        self.m2m_other_specify(
            OTHER, m2m_field='medical_care_access',
            field_other='medical_care_access_other')
        return cleaned_data

    class Meta:
        model = AccessToCare
        fields = '__all__'
