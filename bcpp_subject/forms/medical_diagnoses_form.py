from bcpp_subject_form_validators import MedicalDiagnosesFormValidator

from ..constants import ANNUAL
from ..models import MedicalDiagnoses
from .form_mixins import SubjectModelFormMixin


class MedicalDiagnosesForm (SubjectModelFormMixin):

    form_validator_cls = MedicalDiagnosesFormValidator

    optional_labels = {
        ANNUAL: {'diagnoses': (
            'Since we spoke with you at our last visit, '
            'do you recall or is there a record '
            'of having any of the following serious illnesses?'),
        }
    }

    class Meta:
        model = MedicalDiagnoses
        fields = '__all__'
