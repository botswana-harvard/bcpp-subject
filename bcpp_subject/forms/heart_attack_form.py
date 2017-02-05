from ..models import HeartAttack
from .form_mixins import SubjectModelFormMixin


class HeartAttackForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.validate_other_specify('heart_attack_dx')
        return cleaned_data

    class Meta:
        model = HeartAttack
        fields = '__all__'
