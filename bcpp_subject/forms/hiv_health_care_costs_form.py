from edc_constants.constants import YES

from ..models import HivHealthCareCosts
from .form_mixins import SubjectModelFormMixin


class HivHealthCareCostsForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(HivHealthCareCostsForm, self).clean()

        self.applicable_if(
            YES, field='hiv_medical_care', field_applicable='reason_no_care')
        self.applicable_if(
            YES, field='hiv_medical_care', field_applicable='place_care_received')
        self.applicable_if(
            YES, field='hiv_medical_care', field_applicable='care_regularity')
        self.applicable_if(
            YES, field='hiv_medical_care', field_applicable='doctor_visits')

        return cleaned_data

    class Meta:
        model = HivHealthCareCosts
        fields = '__all__'
