from bcpp_subject_form_validators import CeaOpdFormValidator

from ..models import CeaOpd
from .form_mixins import SubjectModelFormMixin


class CeaOpdForm (SubjectModelFormMixin):

    form_validator_cls = CeaOpdFormValidator

    class Meta:
        model = CeaOpd
        fields = '__all__'
