from edc_constants.constants import NONE

from ..constants import ANNUAL, CANCER, HEART_DISEASE, TUBERCULOSIS, STI
from ..models import MedicalDiagnoses
from .form_mixins import SubjectModelFormMixin


class MedicalDiagnosesForm (SubjectModelFormMixin):

    optional_labels = {
        ANNUAL: {'diagnoses': (
            'Since we spoke with you at our last visit, '
            'do you recall or is there a record '
            'of having any of the following serious illnesses?'),
        }
    }

    def clean(self):
        cleaned_data = super(MedicalDiagnosesForm, self).clean()

        if cleaned_data.get('diagnoses'):
            self.m2m_single_selection_if(NONE, m2m_field='diagnoses')
            diagnoses = []
            for diagnosis in cleaned_data.get('diagnoses'):
                diagnoses.append(diagnosis.short_name)
            self.required_if_true(
                HEART_DISEASE in diagnoses,
                field_required='heart_attack_record')
            self.required_if_true(
                CANCER in diagnoses,
                field_required='cancer_record')
            self.required_if_true(
                TUBERCULOSIS in diagnoses,
                field_required='tb_record')
            self.required_if_true(
                STI in diagnoses,
                field_required='sti_record')
        return cleaned_data

    class Meta:
        model = MedicalDiagnoses
        fields = '__all__'
