from bcpp_subject_form_validators import SexualBehaviourFormValidator as BaseFormValidator

from ..models import SexualBehaviour
from .form_mixins import SubjectModelFormMixin


class SexualBehaviourFormValidator(BaseFormValidator):

    sexual_behaviour_model = 'bcpp_subject.sexualbehaviour'


class SexualBehaviourForm (SubjectModelFormMixin):

    form_validator_cls = SexualBehaviourFormValidator

    class Meta:
        model = SexualBehaviour
        fields = '__all__'
