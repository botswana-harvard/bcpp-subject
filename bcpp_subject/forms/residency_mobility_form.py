from django import forms

from edc_constants.constants import YES

from ..constants import ANNUAL, ZERO
from ..models import ResidencyMobility
from .form_mixins import SubjectModelFormMixin


class ResidencyMobilityForm (SubjectModelFormMixin):

    optional_attrs = {ANNUAL: {
        'help_text': {'permanent_resident': (
            'If participant has moved into the community in the past 12 months,'
            'then since moving in has the participant typically spent more than'
            '14 nights per month in this community.'),
        }
    }}

    def clean(self):
        cleaned_data = super(ResidencyMobilityForm, self).clean()
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = ResidencyMobility(**self.cleaned_data)
        # validating that residency status is not changed after capturing
        # enrollment checklist
        instance.hic_enrollment_checks(forms.ValidationError)
        # validating residency + nights away. redmine 126
        if (cleaned_data.get('permanent_resident') == YES and
                cleaned_data.get('nights_away') == 'more than 6 months'):
            raise forms.ValidationError({
                'nights_away':
                'Participant has spent 14 or more nights per month '
                'in this community, nights away can\'t be '
                'more than 6 months.'})

        self.not_applicable_if(ZERO, 'nights_away', 'cattle_postlands')
        self.validate_other_specify(
            'cattle_postlands', other_stored_value='Other community')

#         # this as in redmine issue 69
#         if (cleaned_data.get('nights_away') == 'zero' and
#                 cleaned_data.get('cattle_postlands') != NOT_APPLICABLE):
#             raise forms.ValidationError(
#                 'If participant spent zero nights away, times spent away should'
#                 'be Not applicable')
#         if (cleaned_data.get('nights_away') != 'zero' and
#                 cleaned_data.get('cattle_postlands') == NOT_APPLICABLE):
#             raise forms.ValidationError(
#                 'Participant has spent more than zero nights away, times spent away'
#                 'CANNOT be Not applicable')
        return cleaned_data

    class Meta:
        model = ResidencyMobility
        fields = '__all__'
