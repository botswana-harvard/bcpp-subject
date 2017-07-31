from bcpp_subject_form_validators import HivLinkageToCareFormValidator as BaseFormValidator

from ..models import HivLinkageToCare
from .form_mixins import SubjectModelFormMixin


class HivLinkageToCareFormValidator(BaseFormValidator):

    hiv_care_adherence_model = 'bcpp_subject.hivcareadherence'


class HivLinkageToCareForm (SubjectModelFormMixin):

    form_validator_cls = HivLinkageToCareFormValidator

    class Meta:
        model = HivLinkageToCare
        fields = '__all__'
