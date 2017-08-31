from bcpp_subject_form_validators import HivUntestedFormValidator as BaseValidator

from ..models import HivUntested
from .form_mixins import SubjectModelFormMixin


class HivUntestedFormValidator(BaseValidator):

    hiv_testing_history_model = 'bcpp_subject.hivtestinghistory'


class HivUntestedForm (SubjectModelFormMixin):

    form_validator_cls = HivUntestedFormValidator

    class Meta:
        model = HivUntested
        fields = '__all__'
