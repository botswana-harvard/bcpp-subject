from edc_constants.constants import DWTA, OTHER

from ..models import CommunityEngagement

from .form_mixins import SubjectModelFormMixin


class CommunityEngagementForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.m2m_single_selection_if(DWTA, m2m_field='problems_engagement')
        self.m2m_other_specify(
            OTHER,
            m2m_field='problems_engagement',
            field_other='problems_engagement_other')
        return cleaned_data

    class Meta:
        model = CommunityEngagement
        fields = '__all__'
