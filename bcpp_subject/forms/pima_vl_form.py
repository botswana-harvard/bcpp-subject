from edc_constants.constants import YES

from ..models import PimaVl
from .form_mixins import SubjectModelFormMixin, MobileTestModelFormMixin


class PimaVlForm (MobileTestModelFormMixin, SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(PimaVlForm, self).clean()
        self.applicable_if(YES, field='test_done', field_applicable='location')
        self.required_if(
            YES, field='test_done', field_required='test_datetime')
        self.required_if(YES, field='test_done', field_required='easy_of_use')
        self.required_if(YES, field='test_done', field_required='stability')
        return cleaned_data

    class Meta:
        model = PimaVl
        fields = '__all__'
