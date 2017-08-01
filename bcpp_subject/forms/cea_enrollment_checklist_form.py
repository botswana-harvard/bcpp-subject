from bcpp_subject_form_validators import CeaEnrollmentChecklistFormValidator

from ..models import CeaEnrollmentChecklist
from .form_mixins import SubjectModelFormMixin


class CeaEnrollmentChecklistForm (SubjectModelFormMixin):

    form_validator_cls = CeaEnrollmentChecklistFormValidator

    class Meta:
        model = CeaEnrollmentChecklist
        fields = '__all__'
