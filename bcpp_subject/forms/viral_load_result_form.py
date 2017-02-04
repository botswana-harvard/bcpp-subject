from ..models import ViralLoadResult
from .form_mixins import SubjectModelFormMixin


class ViralLoadResultForm (SubjectModelFormMixin):

    class Meta:
        model = ViralLoadResult
        fields = '__all__'
