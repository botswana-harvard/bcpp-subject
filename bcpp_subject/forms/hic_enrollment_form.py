from bcpp_subject_form_validators import HicEnrollmentFormValidator

from ..models import HicEnrollment
from .form_mixins import SubjectModelFormMixin


class HicEnrollmentForm (SubjectModelFormMixin):

    form_validator_cls = HicEnrollmentFormValidator

    class Meta:
        model = HicEnrollment
        fields = '__all__'
