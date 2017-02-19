from django import forms

from edc_constants.constants import YES, NO

from ..constants import RESEARCH_BLOOD_DRAW, VIRAL_LOAD, MICROTUBE, BLOOD
from ..models import SubjectRequisition
from .form_mixins import SubjectModelFormMixin


class SubjectRequisitionForm(SubjectModelFormMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not kwargs.get('instance'):
            self.fields['item_type'].initial = 'tube'
            self.fields['item_count'].initial = 1
            self.fields['estimated_volume'].initial = 5.0
        self.fields['panel_name'].widget.attrs['readonly'] = True

    specimen_type = forms.Field(
        initial=BLOOD,
        label='Specimen Type',
        disabled=True)

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('packed') != self.instance.packed:
            raise forms.ValidationError({
                'packed':
                'Value may not be changed here.'})
        elif cleaned_data.get('processed') != self.instance.processed:
            raise forms.ValidationError({
                'processed':
                'Value may not be changed here.'})
        elif not cleaned_data.get('received') and self.instance.received:
            if self.instance.processed:
                raise forms.ValidationError({
                    'received':
                    'Specimen has already been processed.'})
        elif cleaned_data.get('received') and not self.instance.received:
            raise forms.ValidationError({
                'received':
                'Receive specimens in the lab section of the EDC.'})
        elif self.instance.received:
            raise forms.ValidationError(
                'Requisition may not be changed. The specimen has '
                'already been received.')

        self.applicable_if(
            NO, field='is_drawn', field_applicable='reason_not_drawn')
        self.required_if(
            YES, field='is_drawn', field_required='drawn_datetime')
        self.applicable_if(
            YES, field='is_drawn', field_applicable='item_type')
        self.required_if(
            YES, field='is_drawn', field_required='item_count')
        self.required_if(
            YES, field='is_drawn', field_required='estimated_volume')

        if cleaned_data.get('is_drawn'):
            panel_name = cleaned_data.get('panel_name')
            estimated_volume = cleaned_data.get('estimated_volume')
            if panel_name in [RESEARCH_BLOOD_DRAW, VIRAL_LOAD]:
                if (estimated_volume and (
                        estimated_volume < 8.0 or estimated_volume > 10.0)):
                    raise forms.ValidationError({
                        'estimated_volume':
                        'The estimated volume should between 8.0 and 10.0 ml.'})
            elif panel_name == MICROTUBE:
                if (estimated_volume and (
                        estimated_volume < 3.0 or estimated_volume > 5.0)):
                    raise forms.ValidationError({
                        'estimated_volume':
                        'The estimated volume should between 3.0 and 5.0 ml.'})

        return cleaned_data

    class Meta:
        model = SubjectRequisition
        fields = '__all__'
