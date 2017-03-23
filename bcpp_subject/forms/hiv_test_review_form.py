from django import forms
from django.conf import settings
from django.utils import timezone

from ..models import HivTestReview

from .form_mixins import (
    SubjectModelFormMixin, HivTestFormMixin, PreviousAppointmentFormMixin)


class HivTestReviewForm (PreviousAppointmentFormMixin, HivTestFormMixin,
                         SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        self.validate_hiv_test_date()
        return cleaned_data

    def validate_hiv_test_date(self):
        cleaned_data = self.cleaned_data
        hiv_test_date = cleaned_data.get('hiv_test_date')
        if hiv_test_date and hiv_test_date == timezone.now().date():
            raise forms.ValidationError({
                'hiv_test_date': 'Cannot be today\'s date.'})
        elif (hiv_test_date and self.previous_appointment_rdate
              and hiv_test_date < self.previous_appointment_rdate.to(
                  settings.TIME_ZONE).date()):
            raise forms.ValidationError({
                'hiv_test_date':
                'Cannot be on or before last visit on {}.'.format(
                    self.previous_appointment_rdate.to(
                        settings.TIME_ZONE).date().strftime('%Y-%m-%d'))})

        return hiv_test_date

    class Meta:
        model = HivTestReview
        fields = '__all__'
