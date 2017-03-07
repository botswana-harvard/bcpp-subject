from ..models import RecentPartner
from .form_mixins import SubjectModelFormMixin, SexualPartnerFormMixin


class RecentPartnerForm(SexualPartnerFormMixin, SubjectModelFormMixin):

    class Meta:
        model = RecentPartner
        fields = '__all__'
