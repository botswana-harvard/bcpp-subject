from edc_lab.modelform_mixins import RequisitionFormMixin

from ..models import SubjectRequisition
from .form_mixins import SubjectModelFormMixin


class SubjectRequisitionForm(RequisitionFormMixin, SubjectModelFormMixin):

    class Meta:
        model = SubjectRequisition
        fields = '__all__'
