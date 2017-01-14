from django import forms

from ..models import SubjectRequisition

from .form_mixins import SubjectModelFormMixin
from ..constants import RESEARCH_BLOOD_DRAW, VIRAL_LOAD, MICROTUBE


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
        return cleaned_data

    class Meta:
        model = SubjectRequisition
        fields = '__all__'
