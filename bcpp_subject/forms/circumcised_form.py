from bcpp_subject_form_validators import CircumcisedFormValidator

from ..models import Circumcised
from .form_mixins import SubjectModelFormMixin


class CircumcisedForm (SubjectModelFormMixin):

    form_validator_cls = CircumcisedFormValidator

    class Meta:
        model = Circumcised
        fields = '__all__'
