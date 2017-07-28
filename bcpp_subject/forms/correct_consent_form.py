from django import forms
from django.forms import ValidationError

from ..models import CorrectConsent


class CorrectConsentForm(forms.ModelForm):

    def clean(self):
        # FIXME:
        cleaned_data = super().clean()
        self.instance.compare_old_fields_to_consent(
            CorrectConsent(**cleaned_data), ValidationError)
        return cleaned_data

    class Meta:
        model = CorrectConsent
        fields = '__all__'
