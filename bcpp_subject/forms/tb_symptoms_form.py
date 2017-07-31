from ..models import TbSymptoms

from .form_mixins import SubjectModelFormMixin


class TbSymptomsForm (SubjectModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = TbSymptoms
        fields = '__all__'
