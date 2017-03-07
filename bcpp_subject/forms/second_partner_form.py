from ..models import SecondPartner
from .form_mixins import SubjectModelFormMixin, SexualPartnerFormMixin


class SecondPartnerForm(SexualPartnerFormMixin, SubjectModelFormMixin):

    class Meta:
        model = SecondPartner
        fields = '__all__'
