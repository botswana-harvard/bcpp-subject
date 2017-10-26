# from bcpp_subject_form_validators import CeaOpdFormValidator

from ..models import CeaOpd
from .form_mixins import SubjectModelFormMixin


class CeaOpdForm (SubjectModelFormMixin):

    pass

    class Meta:
        model = CeaOpd
        fields = '__all__'
