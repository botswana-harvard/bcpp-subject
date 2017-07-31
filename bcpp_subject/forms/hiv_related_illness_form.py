from bcpp_subject_form_validators import HivRelatedIllnessFormValidator

from ..models import HivRelatedIllness
from .form_mixins import SubjectModelFormMixin


class HivRelatedIllnessForm (SubjectModelFormMixin):

    form_validator_cls = HivRelatedIllnessFormValidator

    class Meta:
        model = HivRelatedIllness
        fields = '__all__'
