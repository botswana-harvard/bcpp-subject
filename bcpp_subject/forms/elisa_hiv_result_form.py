from bcpp_subject_form_validators import ElisaHivResultFormValidator as BaseFormValidator

from ..models import ElisaHivResult
from .form_mixins import SubjectModelFormMixin


class ElisaHivResultFormValidator(BaseFormValidator):

    hic_enrollment_model = 'bcpp_subject.hicenrollment'
    subject_requisition_model = 'bcpp_subject.subjectrequisition'


class ElisaHivResultForm (SubjectModelFormMixin):

    form_validator_cls = ElisaHivResultFormValidator

    class Meta:
        model = ElisaHivResult
        fields = '__all__'
