from ..models import HivMedicalCare
from .form_mixins import SubjectModelFormMixin


class HivMedicalCareForm (SubjectModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = HivMedicalCare
        fields = '__all__'
