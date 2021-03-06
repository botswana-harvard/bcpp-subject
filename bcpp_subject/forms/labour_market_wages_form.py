from django import forms

from edc_constants.constants import YES

from ..choices import MONTHLY_INCOME, HOUSEHOLD_INCOME
from ..models import LabourMarketWages, Grant, SubjectLocator
from .form_mixins import SubjectModelFormMixin


class LabourMarketWagesForm (SubjectModelFormMixin):

    form_validator_cls = None

    def clean(self):
        cleaned_data = super().clean()
        try:
            subject_locator = SubjectLocator.objects.get(
                subject_identifier=cleaned_data.get(
                    'subject_visit').subject_identifier)
            if (subject_locator.may_call_work == YES
                    and cleaned_data.get('employed') == 'not working'):
                raise forms.ValidationError(
                    'Participant gave permission to be contacted at WORK '
                    'in the subject locator, but now reports to be '
                    '\'Not Working\'. Either correct this form or change '
                    'answer in the Locator')
        except SubjectLocator.DoesNotExist:
            pass
        self.validate_employed_reason()
        monthly_answer = 0
        for i in range(len(MONTHLY_INCOME)):
            if MONTHLY_INCOME[i][1] == cleaned_data.get('monthly_income'):
                monthly_answer = i
                break
        household_answer = 0
        for j in range(len(HOUSEHOLD_INCOME)):
            if HOUSEHOLD_INCOME[j][1] == cleaned_data.get('household_income'):
                household_answer = j
                break
        if monthly_answer > household_answer:
            raise forms.ValidationError(
                'Amount in household cannot be less than monthly income')
        return cleaned_data

    def validate_employed_reason(self):
        cleaned_data = self.cleaned_data
        employed = ['government sector', 'private sector',
                    'self-employed working on my own',
                    'self-employed with own employees']
        employed_none = ['occupation', 'monthly_income', 'salary_payment']
        if cleaned_data.get('employed') in employed:
            for response in employed_none:
                if cleaned_data.get(response) == 'None':
                    raise forms.ValidationError({
                        response: [
                            'If participant is employed. '
                            'The response cannot be None']})

    class Meta:
        model = LabourMarketWages
        fields = '__all__'


class GrantForm (forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        # grant information required only when participant says YES to
        # receiving grant(s) at some point
        labour_market_wages = cleaned_data.get('labour_market_wages')
        if labour_market_wages.govt_grant == 'No':
            raise forms.ValidationError(
                'Don\'t fill out the Grant information')
        return cleaned_data

    class Meta:
        model = Grant
        fields = '__all__'
