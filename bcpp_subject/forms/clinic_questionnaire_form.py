from ..models import ClinicQuestionnaire

from .form_mixins import SubjectModelFormMixin


class ClinicQuestionnaireForm (SubjectModelFormMixin):

    class Meta:
        model = ClinicQuestionnaire
        fields = '__all__'
