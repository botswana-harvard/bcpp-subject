from bcpp_subject_form_validators import DemographicsFormValidator

from ..models import Demographics
from .form_mixins import SubjectModelFormMixin


class DemographicsForm(SubjectModelFormMixin):

    form_validator_cls = DemographicsFormValidator

    class Meta:
        model = Demographics
        fields = '__all__'
