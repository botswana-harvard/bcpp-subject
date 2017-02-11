from django import forms

from edc_constants.constants import YES, DWTA, NO

from ..constants import ANNUAL
from ..models import SexualBehaviour
from .form_mixins import SubjectModelFormMixin


class SexualBehaviourForm (SubjectModelFormMixin):

    optional_attrs = {ANNUAL: {
        'label': {
            'last_year_partners': (
                'Since we spoke with you at our last visit, '
                'how many different people have you had '
                'sex with? Please remember to include '
                'casual and once-off partners (prostitutes and '
                'truck drivers) as well as long-term '
                'partners (spouses, boyfriends/girlfriends)[If you '
                'can\'t recall the exact number, '
                'please give a best guess]'),
            'more_sex': (
                'Since we spoke with you at our last visit, did you have sex with '
                'somebody living outside of the community? '),
        }
    }}

    def clean(self):
        cleaned_data = super().clean()

        self.not_required_if(
            NO, DWTA, field='ever_sex', field_required='lifetime_sex_partners')
        self.not_required_if(
            NO, DWTA, field='ever_sex', field_required='last_year_partners')

        if (cleaned_data.get('last_year_partners')
                and cleaned_data.get('lifetime_sex_partners')
                and cleaned_data.get('last_year_partners')
                > cleaned_data.get('lifetime_sex_partners')):
            raise forms.ValidationError({
                'last_year_partners':
                'Cannot exceed {} partners from above.'.format(
                    cleaned_data.get('lifetime_sex_partners'))})
        self.required_if(YES, field='ever_sex', field_required='more_sex')
        self.required_if(YES, field='ever_sex', field_required='first_sex')
        self.applicable_if(
            YES, field='ever_sex', field_applicable='first_sex_partner_age')
        self.validate_other_specify(
            'first_sex_partner_age', other_stored_value='gte_19')
        self.required_if(YES, field='ever_sex', field_required='condom')
        self.required_if(YES, field='ever_sex', field_required='alcohol_sex')
        return cleaned_data

    class Meta:
        model = SexualBehaviour
        fields = '__all__'
