from bcpp_subject_form_validators import HivHealthCareCostsFormValidator

from ..models import HivHealthCareCosts
from .form_mixins import SubjectModelFormMixin


class HivHealthCareCostsForm (SubjectModelFormMixin):

    form_validator_cls = HivHealthCareCostsFormValidator

    class Meta:
        model = HivHealthCareCosts
        fields = '__all__'
