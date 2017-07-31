from bcpp_subject_form_validators import UncircumcisedFormValidator

from ..models import Uncircumcised
from .form_mixins import SubjectModelFormMixin


class UncircumcisedForm (SubjectModelFormMixin):

    form_validator_cls = UncircumcisedFormValidator

    class Meta:
        model = Uncircumcised
        fields = '__all__'
