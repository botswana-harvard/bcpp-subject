from django import forms

from ..choices import MEDICATIONS_TAKEN
from ..models import HypertensionCardiovascular

from .form_mixins import SubjectModelFormMixin


class HypertensionCardiovascularForm(SubjectModelFormMixin):

    medications_taken = forms.MultipleChoiceField(
        choices=MEDICATIONS_TAKEN,
        widget=forms.SelectMultiple())

    is_medication_still_given = forms.MultipleChoiceField(
        choices=MEDICATIONS_TAKEN,
        widget=forms.SelectMultiple())

    class Meta:

        model = HypertensionCardiovascular

        fields = '__all__'
