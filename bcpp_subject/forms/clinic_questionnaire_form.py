from ..models import ClinicQuestionnaire
from .form_mixins import SubjectModelFormMixin


class ClinicQuestionnaireForm (SubjectModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = ClinicQuestionnaire
        fields = '__all__'
