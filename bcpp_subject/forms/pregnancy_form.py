from django import forms

from edc_constants.constants import YES

from ..models import Pregnancy, ReproductiveHealth

from .form_mixins import SubjectModelFormMixin


class PregnancyForm (SubjectModelFormMixin):
    def clean(self):
        cleaned_data = super(PregnancyForm, self).clean()
        try:
            pregnancy_status = ReproductiveHealth.objects.get(
                subject_visit=cleaned_data.get('subject_visit'))
        except ReproductiveHealth.DoesNotExist:
            raise forms.ValidationError(
                'Please complete {} first.'.format(ReproductiveHealth._meta.verbose_name))
        else:
            if pregnancy_status.currently_pregnant == YES and not cleaned_data.get('anc_reg'):
                raise forms.ValidationError(
                    {'anc_reg': 'If participant currently pregnant, have they registered for antenatal care?'})
            # if currently pregnant when was the last lnmp
            if pregnancy_status.currently_pregnant == YES and not cleaned_data.get('lnmp'):
                raise forms.ValidationError(
                    {'lnmp': 'If participant currently pregnant, when was the last known menstrual period?'})
        return cleaned_data

    class Meta:
        model = Pregnancy
        fields = '__all__'
