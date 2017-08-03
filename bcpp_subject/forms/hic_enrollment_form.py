from bcpp_subject_form_validators import HicEnrollmentFormValidator as BaseValidator

from ..models import HicEnrollment
from .form_mixins import SubjectModelFormMixin


class HicEnrollmentFormValidator(BaseValidator):

    subject_consent_model = 'bcpp_subject.subjectconsent'
    subject_locator_model = 'bcpp_subject.subjectlocator'
    residency_mobility_model = 'bcpp_subject.residencymobility'
    hiv_result_model = 'bcpp_subject.hivresult'
    elisa_hiv_result_model = 'bcpp_subject.elisahivresult'


class HicEnrollmentForm (SubjectModelFormMixin):

    form_validator_cls = HicEnrollmentFormValidator

    class Meta:
        model = HicEnrollment
        fields = '__all__'
