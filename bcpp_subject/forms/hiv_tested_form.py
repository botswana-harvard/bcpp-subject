from ..models import HivTested
from .form_mixins import SubjectModelFormMixin, HivTestFormMixin


class HivTestedForm (HivTestFormMixin, SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.validate_other_specify('where_hiv_test')
        return cleaned_data

    class Meta:
        model = HivTested
        fields = '__all__'
