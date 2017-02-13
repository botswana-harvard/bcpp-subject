from ..models import HivResultDocumentation

from .form_mixins import SubjectModelFormMixin, HivTestFormMixin


class HivResultDocumentationForm (HivTestFormMixin, SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = HivResultDocumentation
        fields = '__all__'
