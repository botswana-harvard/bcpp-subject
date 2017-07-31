from bcpp_subject_form_validators import HivUntestedFormValidator

from ..models import HivUntested
from .form_mixins import SubjectModelFormMixin


class HivUntestedForm (SubjectModelFormMixin):

    form_validator_cls = HivUntestedFormValidator

    class Meta:
        model = HivUntested
        fields = '__all__'
