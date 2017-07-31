from bcpp_subject_form_validators import Cd4HistoryFormValidator

from ..models import Cd4History
from .form_mixins import SubjectModelFormMixin


class Cd4HistoryForm (SubjectModelFormMixin):

    form_validator_cls = Cd4HistoryFormValidator

    class Meta:
        model = Cd4History
        fields = '__all__'
