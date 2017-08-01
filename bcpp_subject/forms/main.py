from ..models import QualityOfLife, SubstanceUse

from .form_mixins import SubjectModelFormMixin


class QualityOfLifeForm (SubjectModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = QualityOfLife
        fields = '__all__'


class SubstanceUseForm (SubjectModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = SubstanceUse
        fields = '__all__'
