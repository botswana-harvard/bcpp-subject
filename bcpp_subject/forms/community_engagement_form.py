from django import forms

from ..exceptions import CommunityEngagementError

from ..models import CommunityEngagement

from .form_mixins import SubjectModelFormMixin


class CommunityEngagementForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(CommunityEngagementForm, self).clean()
        try:
            the_problems_list = []
            for problems in cleaned_data.get('problems_engagement'):
                the_problems_list.append(problems.name)
            if 'Don\'t want to answer' in the_problems_list and len(cleaned_data.get('problems_engagement')) > 1:
        except(CommunityEngagementError)as e:
            raise forms.ValidationError(str(e))
        return cleaned_data

    class Meta:
        model = CommunityEngagement
        fields = '__all__'
