from bcpp_subject_form_validators import PimaCd4FormValidator

from ..models import PimaCd4
from .form_mixins import SubjectModelFormMixin


class PimaCd4Form (SubjectModelFormMixin):

    form_validator_cls = PimaCd4FormValidator

    class Meta:
        model = PimaCd4
        fields = '__all__'
