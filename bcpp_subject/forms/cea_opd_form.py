from ..models import CeaOpd
from .form_mixins import SubjectModelFormMixin


class CeaOpdForm (SubjectModelFormMixin):
    pass

    class Meta:
        model = CeaOpd
        fields = '__all__'
