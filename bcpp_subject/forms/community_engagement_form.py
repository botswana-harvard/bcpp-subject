from edc_constants.constants import DWTA, OTHER
from bcpp_subject_form_validators import CommunityEngagementFormValidator

from ..models import CommunityEngagement

from .form_mixins import SubjectModelFormMixin


class CommunityEngagementForm (SubjectModelFormMixin):

    form_validator_cls = CommunityEngagementFormValidator

    class Meta:
        model = CommunityEngagement
        fields = '__all__'
