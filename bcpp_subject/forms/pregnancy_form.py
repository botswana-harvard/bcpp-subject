from django import forms

from edc_constants.constants import YES

from ..models import Pregnancy, ReproductiveHealth

from .form_mixins import SubjectModelFormMixin


class PregnancyForm (SubjectModelFormMixin):
    def clean(self):
        cleaned_data = super(PregnancyForm, self).clean()
        pregnancy_status = ReproductiveHealth.objects.get(subject_visit=cleaned_data.get('subject_visit'))
        if pregnancy_status.currently_pregnant == YES and not cleaned_data.get('anc_reg'):
            raise forms.ValidationError('If participant currently pregnant, have they registered for antenatal care?')
        # if currently pregnant when was the last lnmp
        if pregnancy_status.currently_pregnant == YES and not cleaned_data.get('lnmp'):
            raise forms.ValidationError('If participant currently pregnant, when was the last known menstrual period?')
        return cleaned_data

    class Meta:
        model = Pregnancy
        fields = '__all__'
