from django import forms

from ..models import ClinicQuestionnaire

from .form_mixins import SubjectModelFormMixin


class ClinicQuestionnaireForm (SubjectModelFormMixin):
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = ClinicQuestionnaire
        fields = '__all__'
