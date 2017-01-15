from django import forms

from ..constants import RESEARCH_BLOOD_DRAW, VIRAL_LOAD, MICROTUBE
from ..models import SubjectRequisition

from edc_constants.constants import YES
from .form_mixins import SubjectModelFormMixin


class SubjectRequisitionForm(SubjectModelFormMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'

    def clean(self):
        cleaned_data = super().clean()
        panel = cleaned_data.get('panel_name')
        if panel:
            estimated_volume = cleaned_data.get('estimated_volume')
            if panel in [RESEARCH_BLOOD_DRAW, VIRAL_LOAD]:
                if (estimated_volume < 8.0 or estimated_volume > 10.0):
                    raise forms.ValidationError("The estimated volume should between 8.0 and 10.0 ml.")
            elif panel == MICROTUBE:
                if (estimated_volume < 3.0 or estimated_volume > 5.0):
                    raise forms.ValidationError("The estimated volume should between 3.0 and 5.0 ml.")
        if cleaned_data.get('is_drawn') == YES and cleaned_data.get('reason_not_drawn'):
            raise forms.ValidationError("Cannot provide reasons not drawn for a drawn panel")
        return cleaned_data

    class Meta:
        model = SubjectRequisition
        fields = '__all__'
