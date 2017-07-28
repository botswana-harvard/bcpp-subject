from ..models import HivUntested
from .form_mixins import SubjectModelFormMixin, HivTestFormMixin


class HivUntestedForm (HivTestFormMixin, SubjectModelFormMixin):

    class Meta:
        model = HivUntested
        fields = '__all__'
