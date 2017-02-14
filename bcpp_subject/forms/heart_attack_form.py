from edc_constants.constants import OTHER

from ..models import HeartAttack
from .form_mixins import SubjectModelFormMixin


class HeartAttackForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.m2m_other_specify(
            OTHER, field='dx_heart_attack', m2m_field='dx_heart_attack_other')
        return cleaned_data

    class Meta:
        model = HeartAttack
        fields = '__all__'
