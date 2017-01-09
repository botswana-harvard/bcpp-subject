from django import forms

from edc_consent.modelform_mixins import RequiresConsentModelFormMixin

from ..models import SubjectVisit


class SubjectVisitForm (RequiresConsentModelFormMixin, forms.ModelForm):

    class Meta:
        model = SubjectVisit
        fields = '__all__'
