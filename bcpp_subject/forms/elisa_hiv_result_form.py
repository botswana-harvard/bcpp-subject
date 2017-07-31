from django import forms
from edc_constants.constants import NEG, POS

from ..models import ElisaHivResult
from .form_mixins import SubjectModelFormMixin


class ElisaHivResultForm (SubjectModelFormMixin):

    form_validator_cls = None

    def clean(self):
        cleaned_data = super().clean()
        instance = None
        if self.instance.id:
            instance = self.instance
        else:
            instance = ElisaHivResult(**self.cleaned_data)
        # validating that hiv_result is not changed after HicEnrollment is
        # filled.
        instance.hic_enrollment_checks(forms.ValidationError)
        # validating that a Microtube exists before filling this form.
        instance.elisa_requisition_checks(forms.ValidationError)
        if(cleaned_data.get('hiv_result') in [POS, NEG]
                and not cleaned_data.get('hiv_result_datetime')):
            raise forms.ValidationError({
                'hiv_result_datetime': 'This field is required'})
        return cleaned_data

    class Meta:
        model = ElisaHivResult
        fields = '__all__'
