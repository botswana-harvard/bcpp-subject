from bcpp_subject_form_validators import HivCareAdherenceFormValidator

from ..models import HivCareAdherence
from .form_mixins import SubjectModelFormMixin


class HivCareAdherenceForm(SubjectModelFormMixin):

    form_validator_cls = HivCareAdherenceFormValidator

    class Meta:
        model = HivCareAdherence
        fields = '__all__'
