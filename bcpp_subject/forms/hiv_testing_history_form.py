from django import forms
from django.conf import settings
from edc_constants.constants import YES, POS, NO

from ..models import HivTestingHistory
from .form_mixins import SubjectModelFormMixin, PreviousAppointmentFormMixin
from dateutil.relativedelta import relativedelta


class HivTestingHistoryForm (PreviousAppointmentFormMixin, SubjectModelFormMixin):

    def clean(self):

        cleaned_data = super().clean()

        self.required_if(
            YES, field='has_tested', field_required='when_hiv_test')
        self.validate_when_hiv_test()
        self.required_if(
            YES, field='has_tested', field_required='has_record')
        self.required_if(
            YES, field='has_tested', field_required='verbal_hiv_result')
        self.applicable_if_true(
            cleaned_data.get('has_tested') == YES and cleaned_data.get(
                'verbal_hiv_result') == POS,
            field_applicable='other_record')
        self.applicable_if(
            POS, field='verbal_hiv_result', field_applicable='other_record')
        return cleaned_data

    def validate_when_hiv_test(self):
        cleaned_data = self.cleaned_data
        when = self.cleaned_data.get('when_hiv_test')
        if (cleaned_data.get('has_tested') == NO
                and self.previous_appointment_rdate
                and when):
            formatted_date = self.previous_appointment_rdate.date().strftime(
                '%Y-%m-%d')
            rdelta = relativedelta(
                self.previous_appointment_rdate.to(
                    settings.TIME_ZONE).datetime,
                cleaned_data.get('subject_visit').report_datetime)
            months = abs(rdelta.years * 12 + rdelta.months)
            errmsg = 'Invalid, have not tested since {}. That\'s {} months ago.'.format(
                formatted_date, months)
            if when == 'In the last month' and 0 <= months <= 1:
                raise forms.ValidationError({'when_hiv_test': errmsg})
            elif when == '1 to 5 months ago' and not (1 <= months < 6):
                raise forms.ValidationError({'when_hiv_test': errmsg})
            elif when == '6 to 12 months ago' and not (6 <= months <= 12):
                raise forms.ValidationError({'when_hiv_test': errmsg})
            elif when == 'more than 12 months ago' and not months > 12:
                raise forms.ValidationError({'when_hiv_test': errmsg})

    class Meta:
        model = HivTestingHistory
        fields = '__all__'
