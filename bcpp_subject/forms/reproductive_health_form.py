from edc_base.modelform_validators import FormValidator
from bcpp_subject_form_validators import ReproductiveHealthFormValidator

from ..constants import ANNUAL
from ..models import ReproductiveHealth
from .form_mixins import SubjectModelFormMixin


class ReproductiveHealthForm (SubjectModelFormMixin):

    form_validator_cls = ReproductiveHealthFormValidator

    optional_attrs = {ANNUAL: {
        'label': {'family_planning': (
            'Since we spoke with you at our last visit, have you used any methods'
            'to prevent pregnancy?')}}}

    class Meta:
        model = ReproductiveHealth
        fields = '__all__'
