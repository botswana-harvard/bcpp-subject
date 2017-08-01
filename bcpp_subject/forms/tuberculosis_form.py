from bcpp_subject_form_validators import TuberculosisFormValidator

from ..models import Tuberculosis
from .form_mixins import SubjectModelFormMixin


class TuberculosisForm (SubjectModelFormMixin):

    form_validator_cls = TuberculosisFormValidator

    class Meta:
        model = Tuberculosis
        fields = '__all__'
