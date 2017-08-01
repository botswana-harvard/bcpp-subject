from bcpp_subject_form_validators import ImmigrationStatusFormValidator

from .form_mixins import SubjectModelFormMixin
from ..models import ImmigrationStatus


class ImmigrationStatusForm (SubjectModelFormMixin):

    form_validator_cls = ImmigrationStatusFormValidator

    class Meta:
        model = ImmigrationStatus
        fields = '__all__'
