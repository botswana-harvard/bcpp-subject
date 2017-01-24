from ..models import ArvHistory

from .form_mixins import SubjectModelFormMixin


class ArvHistoryForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = ArvHistory
        fields = '__all__'
