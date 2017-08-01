from bcpp_subject_form_validators import EducationFormValidator as BaseFormValidator

from ..models import Education
from .form_mixins import SubjectModelFormMixin


class EducationFormValidator(BaseFormValidator):

    subject_locator_model = 'bcpp_subject.subjectlocator'


class EducationForm (SubjectModelFormMixin):

    form_validator_cls = EducationFormValidator

    class Meta:
        model = Education
        fields = '__all__'
