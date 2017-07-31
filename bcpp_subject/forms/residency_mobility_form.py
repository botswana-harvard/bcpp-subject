from bcpp_subject_form_validators import ResidencyMobilityFormValidator as BaseFormValidator

from ..constants import ANNUAL
from ..models import ResidencyMobility
from .form_mixins import SubjectModelFormMixin


class ResidencyMobilityFormValidator(BaseFormValidator):

    residency_mobility_model = 'bcpp_subject.residencymobility'


class ResidencyMobilityForm (SubjectModelFormMixin):

    form_validator_cls = ResidencyMobilityFormValidator

    optional_attrs = {ANNUAL: {
        'help_text': {'permanent_resident': (
            'If participant has moved into the community in the past 12 months,'
            'then since moving in has the participant typically spent more than'
            '14 nights per month in this community.'),
        }
    }}

    class Meta:
        model = ResidencyMobility
        fields = '__all__'
