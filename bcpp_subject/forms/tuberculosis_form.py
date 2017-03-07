from ..models import Tuberculosis
from .form_mixins import SubjectModelFormMixin


class TuberculosisForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.validate_other_specify('tb_dx')
        return cleaned_data

    class Meta:
        model = Tuberculosis
        fields = '__all__'
