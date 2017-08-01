from bcpp_subject_form_validators import AccessToCareFormValidator

from ..models import AccessToCare
from .form_mixins import SubjectModelFormMixin


class AccessToCareForm (SubjectModelFormMixin):

    form_validator_cls = AccessToCareFormValidator

    class Meta:
        model = AccessToCare
        fields = '__all__'
