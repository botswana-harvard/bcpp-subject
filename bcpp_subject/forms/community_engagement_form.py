from django import forms

from edc_constants.constants import DWTA

from ..models import CommunityEngagement

from .form_mixins import SubjectModelFormMixin


class CommunityEngagementForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        answers = []
        if cleaned_data.get('problems_engagement'):
            for item in cleaned_data.get('problems_engagement'):
                answers.append(item.name)
            if len(answers) > 1 and DWTA in answers:
                raise forms.ValidationError({
                    'problems_engagement': (
                        'You cannot choose \'Don\'t want to answer\' '
                        'and another problem at the same time. '
                        'Please correct.')})
        return cleaned_data

    class Meta:
        model = CommunityEngagement
        fields = '__all__'
