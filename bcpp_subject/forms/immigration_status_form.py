from ..models import ImmigrationStatus

from .form_mixins import SubjectModelFormMixin


class ImmigrationStatusForm (SubjectModelFormMixin):

    class Meta:
        model = ImmigrationStatus
        fields = '__all__'
