from bcpp_subject_form_validators import HypertensionCardiovascularFormValidator

from ..models import HypertensionCardiovascular
from .form_mixins import SubjectModelFormMixin


class HypertensionCardiovascularForm(SubjectModelFormMixin):

    form_validator_cls = HypertensionCardiovascularFormValidator

    class Meta:

        model = HypertensionCardiovascular
        fields = '__all__'
