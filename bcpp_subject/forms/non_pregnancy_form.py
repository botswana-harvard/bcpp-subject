from ..models import NonPregnancy

from .form_mixins import SubjectModelFormMixin


class NonPregnancyForm (SubjectModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = NonPregnancy
        fields = '__all__'
