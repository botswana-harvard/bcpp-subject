from bcpp_subject_form_validators import CancerFormValidator

from ..models import Cancer
from .form_mixins import SubjectModelFormMixin


class CancerForm (SubjectModelFormMixin):

    form_validator_cls = CancerFormValidator

    class Meta:
        model = Cancer
        fields = '__all__'
