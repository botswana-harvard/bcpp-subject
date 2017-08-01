from ..models import HivResult

from bcpp_subject_form_validators import HivResultFormValidator as BaseFormValidator
from bcpp_labs.labs import microtube_panel

from .form_mixins import SubjectModelFormMixin


class HivResultFormValidator(BaseFormValidator):

    hic_enrollment_model = 'bcpp_subject.hicenrollment'
    subject_requisition_model = 'bcpp_subject.subjectrequisition'
    microtube_panel_name = microtube_panel.name


class HivResultForm(SubjectModelFormMixin):

    form_validator_cls = HivResultFormValidator

    class Meta:
        model = HivResult
        fields = '__all__'
