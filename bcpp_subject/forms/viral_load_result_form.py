from ..models import ViralLoadResult
from .form_mixins import SubjectModelFormMixin


class ViralLoadResultForm (SubjectModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = ViralLoadResult
        fields = '__all__'
