from django import forms

from bcpp_subject_form_validators import SubjectLocatorFormValidator as BaseFormValidator

from ..models import SubjectLocator
from .form_mixins import SubjectModelFormMixin
from edc_constants.choices import YES_NO


class SubjectLocatorFormValidator(BaseFormValidator):

    hic_enrollment_model = 'bcpp_subject.hicenrollment'


class SubjectLocatorForm (SubjectModelFormMixin):

    form_validator_cls = SubjectLocatorFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['home_visit_permission'].label = (
            'Has the participant given his/her permission for study'
            'staff to make home visits for follow-up purposes '
            '(such as return of test results, contact about future '
            'studies or sharing BCPP results)?')
        self.fields['may_follow_up'].label = (
            'Has the participant given his/her permission for study staff '
            'to call her for follow-up purposes during the study?'
            '(such as return of test results, contact about future '
            'studies or sharing BCPP results)?')

    subject_identifier = forms.CharField(
        label='Subject identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = SubjectLocator
        fields = '__all__'
