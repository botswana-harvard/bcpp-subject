from .form_mixins import SubjectModelFormMixin
from ..models import ImmigrationStatus


class ImmigrationStatusForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.validate_other('country_of_origin', 'country_of_origin_other')
        return cleaned_data

    class Meta:
        model = ImmigrationStatus
        fields = '__all__'
