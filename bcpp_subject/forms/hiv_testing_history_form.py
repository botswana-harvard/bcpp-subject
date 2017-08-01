from bcpp_subject_form_validators import HivTestingHistoryFormValidator

from ..models import HivTestingHistory
from .form_mixins import SubjectModelFormMixin


class HivTestingHistoryForm (SubjectModelFormMixin):

    form_validator_cls = HivTestingHistoryFormValidator

    class Meta:
        model = HivTestingHistory
        fields = '__all__'
