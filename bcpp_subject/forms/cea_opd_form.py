from ..models import CeaOpd
from .form_mixins import SubjectModelFormMixin
from bcpp_subject_form_validators.form_validators import CeaOpdFormValidator


class CeaOpdForm (SubjectModelFormMixin):

    form_validator_cls = CeaOpdFormValidator

    class Meta:
        model = CeaOpd
        fields = '__all__'
