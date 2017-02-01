from django import forms

from edc_constants.constants import YES, NO

from ..models import HivUntested
from .form_mixins import SubjectModelFormMixin


class HivUntestedForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(HivUntestedForm, self).clean()
        # if no, don't answer next question
        if cleaned_data.get('hiv_pills') == NO and cleaned_data.get('arvs_hiv_test'):
            raise forms.ValidationError(
                'You are answering information about ARV\'s '
                'yet have answered \'NO\', patient has '
                'never heard about ARV\'s. Please correct')
        if cleaned_data.get('hiv_pills') == YES and not cleaned_data.get('arvs_hiv_test'):
            raise forms.ValidationError(
                'If participant has heard about ARV\'s, give answer whether '
                'participant believes that HIV positive people '
                'can live longer if they take ARV\'s')
        if cleaned_data.get('not sure') and not cleaned_data.get('arvs_hiv_test'):
            raise forms.ValidationError(
                'Even if participant is not sure, provide answer whether '
                'participant believes that HIV positive people can '
                'live longer if they take ARV\'s')
        return cleaned_data

    class Meta:
        model = HivUntested
        fields = '__all__'
