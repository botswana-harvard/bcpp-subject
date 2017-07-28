from ..models import HivResultDocumentation

from .form_mixins import SubjectModelFormMixin, HivTestFormMixin


class HivResultDocumentationForm (HivTestFormMixin, SubjectModelFormMixin):

    class Meta:
        model = HivResultDocumentation
        fields = '__all__'
