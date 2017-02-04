from django import forms

from ..models import SubjectReferral
from .form_mixins import SubjectModelFormMixin
from ..referral import get_required_crf


class SubjectReferralForm(SubjectModelFormMixin):

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
