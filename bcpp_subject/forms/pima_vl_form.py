from bcpp_subject_form_validators import PimaVlFormValidator

from ..models import PimaVl
from .form_mixins import SubjectModelFormMixin


class PimaVlForm (SubjectModelFormMixin):

    form_validator_cls = PimaVlFormValidator

    class Meta:
        model = PimaVl
        fields = '__all__'
