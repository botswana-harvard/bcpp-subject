from bcpp_subject_form_validators import HeartAttackFormValidator

from ..models import HeartAttack
from .form_mixins import SubjectModelFormMixin


class HeartAttackForm (SubjectModelFormMixin):

    form_validator_cls = HeartAttackFormValidator

    class Meta:
        model = HeartAttack
        fields = '__all__'
