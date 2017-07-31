from django import forms

from edc_constants.constants import YES, NO
from bcpp_subject_form_validators import EducationFormValidator as BaseFormValidator

from ..models import Education, SubjectLocator
from .form_mixins import SubjectModelFormMixin


class EducationFormValidator(BaseFormValidator):

    subject_locator_model = 'bcpp_subject.subjectlocator'


class EducationForm (SubjectModelFormMixin):

    form_validator_cls = EducationFormValidator

    def clean(self):
        cleaned_data = super().clean()
        # validating not working
        # FIXME: Then fix it!
        try:
            subject_locator = SubjectLocator.objects.get(
                subject_identifier=cleaned_data.get(
                    'subject_visit').subject_identifier)
            if (subject_locator.may_call_work == YES
                    and cleaned_data.get('working') == NO):
                raise forms.ValidationError(
                    'Participant gave permission to be contacted at WORK in '
                    'the subject locator but now reports to be \'Not Working\'. '
                    'Either correct this form or change '
                    'answer in the Locator')
        except SubjectLocator.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = Education
        fields = '__all__'
