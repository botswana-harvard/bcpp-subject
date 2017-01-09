from django import forms

from ..models import SubjectRequisition

from .form_mixins import SubjectModelFormMixin


class SubjectRequisitionForm(SubjectModelFormMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_type'].initial = 'tube'

    def clean(self):
        cleaned_data = super().clean()
        panel = cleaned_data.get('panel')
        if panel:
            estimated_volume = cleaned_data.get('estimated_volume')
            if panel.name in ['Research Blood Draw', 'Viral Load']:
                if (estimated_volume < 8.0 or estimated_volume > 10.0):
                    raise forms.ValidationError("The estimated volume should between 8.0 and 10.0 ml.")
            elif panel.name == 'Microtube':
                if (estimated_volume < 3.0 or estimated_volume > 5.0):
                    raise forms.ValidationError("The estimated volume should between 3.0 and 5.0 ml.")
        return cleaned_data

    class Meta:
        model = SubjectRequisition
        fields = '__all__'
