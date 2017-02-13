from edc_constants.constants import YES, POS

from ..models import HivTestingHistory
from .form_mixins import SubjectModelFormMixin


class HivTestingHistoryForm (SubjectModelFormMixin):

    def clean(self):

        cleaned_data = super(HivTestingHistoryForm, self).clean()

        self.required_if(
            YES, field='has_tested', field_required='when_hiv_test')
        self.required_if(
            YES, field='has_tested', field_required='when_hiv_test')
        self.required_if(
            YES, field='has_tested', field_required='verbal_hiv_result')
        self.applicable_if(
            YES, field='has_tested', field_applicable='other_record')
        self.applicable_if(
            POS, field='verbal_hiv_result', field_applicable='other_record')
        return cleaned_data

    class Meta:
        model = HivTestingHistory
        fields = '__all__'
