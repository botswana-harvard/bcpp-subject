from ..models import ArvHistory

from .form_mixins import SubjectModelFormMixin


class ArvHistoryForm (SubjectModelFormMixin):

    # FIXME: validate that the ARV codes selected are not the same
    #        as any referred to on HivCareAdherence
    # FIXME: validate date stopped is less than date started

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = ArvHistory
        fields = '__all__'
