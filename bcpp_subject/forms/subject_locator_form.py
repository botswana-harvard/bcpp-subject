from django import forms

from bcpp_subject_form_validators import SubjectLocatorFormValidator as BaseFormValidator

from ..models import SubjectLocator
from .form_mixins import SubjectModelFormMixin


class SubjectLocatorFormValidator(BaseFormValidator):

    hic_enrollment_model = 'bcpp_subject.hicenrollment'


class SubjectLocatorForm (SubjectModelFormMixin):

    form_validator_cls = SubjectLocatorFormValidator

    subject_identifier = forms.CharField(
        label='Subject identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = SubjectLocator
        fields = '__all__'
