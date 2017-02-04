from ..models import HivUntested
from .form_mixins import SubjectModelFormMixin


class HivUntestedForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = HivUntested
        fields = '__all__'
