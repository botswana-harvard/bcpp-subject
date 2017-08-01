from bcpp_subject_form_validators import HivResultDocumentationFormValidator as BaseFormValidator

from ..models import HivResultDocumentation
from .form_mixins import SubjectModelFormMixin


class HivResultDocumentationFormValidator(BaseFormValidator):

    hiv_testing_history_model = 'bcpp_subject.hivtestinghistory'


class HivResultDocumentationForm(SubjectModelFormMixin):

    form_validator_cls = HivResultDocumentationFormValidator

    class Meta:
        model = HivResultDocumentation
        fields = '__all__'
