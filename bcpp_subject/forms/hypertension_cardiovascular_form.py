from ..models import HypertensionCardiovascular

from .form_mixins import SubjectModelFormMixin


class HypertensionCardiovascularForm(SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:

        model = HypertensionCardiovascular
        fields = '__all__'
