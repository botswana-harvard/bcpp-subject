from ..models import Cancer
from .form_mixins import SubjectModelFormMixin


class CancerForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.validate_other_specify('cancer_dx')
        return cleaned_data

    class Meta:
        model = Cancer
        fields = '__all__'
