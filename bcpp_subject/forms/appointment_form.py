from django import forms

from edc_appointment.modelform_mixins import AppointmentFormMixin

from ..models import Appointment, SubjectLocator


class AppointmentForm(AppointmentFormMixin, forms.ModelForm):

    @property
    def required_additional_forms_exist(self):
        """Returns True if any required additional forms are yet to be keyed.
        """
        try:
            obj = SubjectLocator.objects.get(
                subject_identifier=self.instance.subject_identifier)
        except SubjectLocator.DoesNotExist:
            obj = None
        return False if obj else True

    class Meta:
        model = Appointment
        fields = '__all__'
