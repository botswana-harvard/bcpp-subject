from edc_lab.forms import RequisitionFormMixin
from bcpp_subject_form_validators import SubjectRequisitionFormValidator

from ..models import SubjectRequisition
from .form_mixins import SubjectModelFormMixin


class SubjectRequisitionForm(RequisitionFormMixin, SubjectModelFormMixin):

    form_validator_cls = SubjectRequisitionFormValidator

    class Meta:
        model = SubjectRequisition
        fields = '__all__'
