from django import forms

from edc_constants.constants import NOT_APPLICABLE, YES, NO

from ..models import Participation
from .form_mixins import SubjectModelFormMixin


class ParticipationForm (SubjectModelFormMixin):

    def clean(self):

        cleaned_data = super().clean()
        if (cleaned_data.get('full') == NO
                and cleaned_data.get('participation_type') == NOT_APPLICABLE):
            raise forms.ValidationError(
                'Participation type cannot be \'Not Applicable\' '
                'if participant is not fully participating in BHS.')
        if (cleaned_data.get('full') == YES
                and cleaned_data.get('participation_type') != 'Not Applicable'):
            raise forms.ValidationError(
                'If full participation is chosen, type of participation '
                'should be \'Not Applicable\'.')

        return cleaned_data

    class Meta:
        model = Participation
        fields = '__all__'
