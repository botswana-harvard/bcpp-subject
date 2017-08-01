from bcpp_subject_form_validators import CircumcisionFormValidator

from ..models import Circumcision
from .form_mixins import SubjectModelFormMixin


class CircumcisionForm (SubjectModelFormMixin):

    form_validator_cls = CircumcisionFormValidator

    class Meta:
        model = Circumcision
        fields = '__all__'
