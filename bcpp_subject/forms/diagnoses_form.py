from django import forms

from ..models import HeartAttack, Cancer, Tuberculosis, Sti

from .form_mixins import SubjectModelFormMixin


class HeartAttackForm (SubjectModelFormMixin):

    class Meta:
        model = HeartAttack
        fields = '__all__'


class CancerForm (SubjectModelFormMixin):

    class Meta:
        model = Cancer
        fields = '__all__'


class TuberculosisForm (SubjectModelFormMixin):

    class Meta:
        model = Tuberculosis
        fields = '__all__'


class StiForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super(StiForm, self).clean()
        # It None in diagnosis, then ensure no date is entered.
        if not cleaned_data.get('sti_dx') or cleaned_data.get('sti_dx')[0].name == 'None':
            attrs = ['wasting_date', 'yeast_infection_date', 'pneumonia_date',
                     'pcp_date', 'herpes_date', 'diarrhoea_date']
            for attr in attrs:
                if cleaned_data.get(attr):
                    # put message on incorrect field
                    raise forms.ValidationError(
                        {attr:
                         'If participant has never had any illness, '
                         'then do not provide any dates.'})
        # wasting
        sti_dx = 'Severe weight loss (wasting) - more than 10% of body weight'
        if cleaned_data.get('sti_dx'):
            if (cleaned_data.get('sti_dx')[0].name == sti_dx and not
                    cleaned_data.get('wasting_date')):
                raise forms.ValidationError(
                    'If participant has ever been diagnosed with wasting, '
                    'what is the date of diagnosis?')
            # diarrhoea
            sti_dx = 'Unexplained diarrhoea for one month'
            if (cleaned_data.get('sti_dx')[0].name == sti_dx and not
                    cleaned_data.get('diarrhoea_date')):
                raise forms.ValidationError(
                    'If participant has ever been diagnosed with diarrhoea, '
                    'what is the diagnosis date?')
            # yesat_infection
            sti_dx = 'Yeast infection of mouth or oesophagus'
            if (cleaned_data.get('sti_dx')[0].name == sti_dx and not
                    cleaned_data.get('yeast_infection_date')):
                raise forms.ValidationError(
                    'If participant has ever been diagnosed with yeast '
                    'infection, what is the diagnosis date?')
            # pneumonia
            sti_dx = 'Severe pneumonia or meningitis or sepsis'
            if (cleaned_data.get('sti_dx')[0].name == sti_dx and not
                    cleaned_data.get('pneumonia_date')):
                raise forms.ValidationError(
                    'If participant has ever been diagnosed with '
                    'pneumonia_date, what is the date of diagnosis?')
            # pcp
            if (cleaned_data.get('sti_dx')[0].name == 'PCP (Pneumocystis pneumonia)' and not
                    cleaned_data.get('pcp_date')):
                raise forms.ValidationError(
                    'If participant has ever been diagnosed with PCP, '
                    'what is the date of diagnosis?')
            # herpes
            sti_dx = 'Herpes infection for more than one month'
            if (cleaned_data.get('sti_dx')[0].name == sti_dx and not
                    cleaned_data.get('herpes_date')):
                raise forms.ValidationError(
                    'If participant has ever been diagnosed with '
                    'Herpes for more than a month, '
                    'what is the date of diagnosis?')
        return cleaned_data

    class Meta:
        model = Sti
        fields = '__all__'
