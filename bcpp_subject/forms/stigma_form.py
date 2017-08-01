from ..models import Stigma, StigmaOpinion, PositiveParticipant

from .form_mixins import SubjectModelFormMixin


class StigmaForm (SubjectModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = Stigma
        fields = '__all__'


class StigmaOpinionForm (SubjectModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = StigmaOpinion
        fields = '__all__'


class PositiveParticipantForm (SubjectModelFormMixin):

    form_validator_cls = None

    class Meta:
        model = PositiveParticipant
        fields = '__all__'
