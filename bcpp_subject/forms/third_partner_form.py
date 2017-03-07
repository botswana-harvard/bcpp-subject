from ..models import ThirdPartner
from .form_mixins import SubjectModelFormMixin, SexualPartnerFormMixin


class ThirdPartnerForm(SexualPartnerFormMixin, SubjectModelFormMixin):

    class Meta:
        model = ThirdPartner
        fields = '__all__'
