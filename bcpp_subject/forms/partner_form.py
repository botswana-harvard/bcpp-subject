from django import forms

from edc_constants.constants import NOT_APPLICABLE, YES, NO, DWTA

from ..models import (
    RecentPartner, SecondPartner, ThirdPartner, SexualBehaviour)
from .form_mixins import SubjectModelFormMixin


class BasePartnerForm (SubjectModelFormMixin):

    yes_no_unsure_options = [YES, NO, 'not sure', DWTA]

    def clean(self):
        """Ensures that question about antiretrovirals is not answered
        if partner is known to be HIV negative.
        """
        cleaned_data = super().clean()
        try:
            subject_behaviour = SexualBehaviour.objects.get(
                subject_visit=cleaned_data.get('subject_visit'))
        except SexualBehaviour.DoesNotExist:
            raise forms.ValidationError(
                'Please complete {} first.'.format(
                    SexualBehaviour._meta.verbose_name))
        else:
            if subject_behaviour.lifetime_sex_partners == 1:
                if cleaned_data.get('concurrent') not in [NO, DWTA]:
                    raise forms.ValidationError({
                        'concurrent': (
                            "You wrote that you have only one partner ever on {}. "
                            "Please correct if you have sex with other partners.".format(
                                SexualBehaviour._meta.verbose_name))})

        if (cleaned_data.get('first_partner_hiv') == 'negative'
                and cleaned_data.get('first_haart') in self.yes_no_unsure_options):
            raise forms.ValidationError(
                'Do not answer this question if partners HIV status is '
                'known to be negative')

        if (cleaned_data.get('first_partner_hiv') == 'I am not sure'
                and cleaned_data.get('first_haart') in self.yes_no_unsure_options):
            raise forms.ValidationError(
                'If partner status is not known, do not give information '
                'about status of ARV\'s')

        self.validate_days_or_months()

        # FIXME: does this work??
        if self.instance.skip_logic_questions(self.cleaned_data.get('first_partner_live')):
            if not cleaned_data.get('sex_partner_community', None) == NOT_APPLICABLE:
                raise forms.ValidationError(
                    'if response in question 3, is In this community or Farm '
                    'within this community or Cattle post within this community. '
                    'The response in the next question is NOT_APPLICABLE')

        self.validate_other_specify(
            'first_exchange2', 'first_exchange2_age_other')

        return cleaned_data

    def validate_days_or_months(self):
        cleaned_data = self.cleaned_data
        for field in ['first_first_sex', 'third_last_sex']:
            if cleaned_data.get(field + '_calc'):
                if (cleaned_data.get(field) == 'Days'):
                    if cleaned_data.get(field + '_calc') > 31:
                        raise forms.ValidationError(
                            {field: 'Cannot exceed 31 days'})
                if (cleaned_data.get(field) == 'Months'):
                    if (cleaned_data.get(field + '_calc') > 12):
                        raise forms.ValidationError(
                            {field: 'Cannot exceed 12 months'})


class RecentPartnerForm(BasePartnerForm):

    class Meta:
        model = RecentPartner
        fields = '__all__'


class SecondPartnerForm(BasePartnerForm):

    class Meta:
        model = SecondPartner
        fields = '__all__'


class ThirdPartnerForm(BasePartnerForm):

    class Meta:
        model = ThirdPartner
        fields = '__all__'
