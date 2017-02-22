from django import forms

from edc_constants.constants import YES, NO

from ..models import SubjectLocator, HicEnrollment
from .form_mixins import SubjectModelFormMixin


class SubjectLocatorForm (SubjectModelFormMixin):

    subject_identifier = forms.CharField(
        label='Subject identifier',
        disabled=True)

    def clean(self):
        cleaned_data = super().clean()

        self.validate_has_contacts_for_hic()

        self.required_if(
            YES, field='home_visit_permission', field_required='physical_address')
        self.required_if(
            YES, field='may_follow_up', field_required='subject_cell')
        self.not_required_if(
            NO, field='may_follow_up', field_required='subject_cell_alt', inverse=False)
        self.not_required_if(
            NO, field='may_follow_up', field_required='subject_phone', inverse=False)
        self.not_required_if(
            NO, field='may_follow_up', field_required='subject_phone_alt', inverse=False)

        return cleaned_data

    def validate_has_contacts_for_hic(self):
        cleaned_data = self.cleaned_data
        try:
            HicEnrollment.objects.get(
                subject_visit__subject_identifier=cleaned_data.get(
                    'subject_identifier'))
        except HicEnrollment.DoesNotExist:
            pass
        else:
            if (not self.subject_cell and not self.subject_cell_alt
                    and not self.subject_phone):
                raise forms.ValidationError(
                    'Subject is enrolled to HIC. Please provide at least one '
                    'contact number.')

    class Meta:
        model = SubjectLocator
        fields = '__all__'
