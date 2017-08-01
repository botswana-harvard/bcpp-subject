from bcpp_subject_form_validators import HivTestedFormValidator as BaseFormValidator

from ..models import HivTested
from .form_mixins import SubjectModelFormMixin


class HivTestedFormValidator(BaseFormValidator):

    hiv_testing_history_model = 'bcpp_subject.hivtestinghistory'


class HivTestedForm (SubjectModelFormMixin):

    form_validator_cls = HivTestedFormValidator

    class Meta:
        model = HivTested
        fields = '__all__'
