from .form_mixins import SubjectModelFormMixin
from ..models import ImmigrationStatus


class ImmigrationStatusForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.validate_other_specify('country_of_origin')
        return cleaned_data

    class Meta:
        model = ImmigrationStatus
        fields = '__all__'
