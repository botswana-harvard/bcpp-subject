from bcpp_subject_form_validators import ResourceUtilizationFormValidator

from ..models import ResourceUtilization
from .form_mixins import SubjectModelFormMixin


class ResourceUtilizationForm (SubjectModelFormMixin):

    form_validator_cls = ResourceUtilizationFormValidator

    class Meta:
        model = ResourceUtilization
        fields = '__all__'
