from django import forms

from ..constants import ANNUAL
from ..exceptions import CircumcisionError
from ..models import Circumcision, Uncircumcised, Circumcised

from .form_mixins import SubjectModelFormMixin


class CircumcisionForm (SubjectModelFormMixin):

    optional_labels = {
        ANNUAL: {'circumcised': (
            'Have you been circumcised since we last spoke with you?'),
        }
    }

    class Meta:
        model = Circumcision
        fields = '__all__'


class CircumcisedForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(CircumcisedForm, self).clean()
        try:
            instance = self._meta.model(id=self.instance.id, **cleaned_data)
            instance.common_clean()
        except (CircumcisionError) as e:
            raise forms.ValidationError(str(e))
        return cleaned_data

    class Meta:
        model = Circumcised
        fields = '__all__'


class UncircumcisedForm (SubjectModelFormMixin):
    def clean(self):

        cleaned_data = super(UncircumcisedForm, self).clean()
        if cleaned_data.get('circumcised') == 'Yes' and not cleaned_data.get('health_benefits_smc'):
            raise forms.ValidationError('if \'YES\', what are the benefits of male circumcision?.')
        return cleaned_data

    class Meta:
        model = Uncircumcised
        fields = '__all__'
