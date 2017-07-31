from bcpp_subject_form_validators import HivTestReviewFormValidator as BaseFormValidator

from ..models import HivTestReview
from .form_mixins import SubjectModelFormMixin


class HivTestReviewFormValidator(BaseFormValidator):

    hiv_testing_history_model = 'bcpp_subject.hivtestinghistory'


class HivTestReviewForm (SubjectModelFormMixin):

    form_validator_cls = HivTestReviewFormValidator

    class Meta:
        model = HivTestReview
        fields = '__all__'
