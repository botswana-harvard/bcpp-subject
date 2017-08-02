from django import forms
from bcpp_referral.utils import get_required_crf
from bcpp_subject_form_validators import SubjectReferralFormValidator

from ..models import SubjectReferral
from .form_mixins import SubjectModelFormMixin


class SubjectReferralForm(SubjectModelFormMixin):

    form_validator_cls = SubjectReferralFormValidator

    def clean(self):
        cleaned_data = super().clean()
        required_crf = get_required_crf(
            subject_visit=cleaned_data.get('subject_visit'))
        if required_crf:
            raise forms.ValidationError(
                'Insufficient information to prepare referral. Complete \'{0}\' first '
                'and try again.'.format(
                    required_crf._meta.verbose_name))
        return cleaned_data

    class Meta:
        model = SubjectReferral
        fields = '__all__'
