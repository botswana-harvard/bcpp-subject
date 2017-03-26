import arrow

from django import forms

from edc_appointment.modelform_mixins import AppointmentFormMixin
from edc_appointment.constants import NEW_APPT
from edc_base.utils import get_utcnow

from ..models import Appointment


class AppointmentForm(AppointmentFormMixin, forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('appt_status') != NEW_APPT:
            appt_datetime = cleaned_data.get('appt_datetime')
            rappt_datetime = arrow.Arrow.fromdatetime(
                appt_datetime, appt_datetime.tzinfo)
            if rappt_datetime.to('UTC').date() > get_utcnow().date():
                raise forms.ValidationError({
                    'appt_datetime': 'Cannot be a future date.'})
        return cleaned_data

    class Meta:
        model = Appointment
        fields = '__all__'
