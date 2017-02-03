from inspect import currentframe

from django import forms

from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE, DWTA

from ..models import HivCareAdherence
from .form_mixins import SubjectModelFormMixin


def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno


class HivCareAdherenceForm(SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()

        # section: care
        self.validate_medical_care()
        self.validate_ever_taken()
        self.validate_art_part1()
        self.validate_art_regimen()
        self.validate_prev_art_regimen()
        self.validate_adherence()
        self.validate_hospitalization_part1()
        self.validate_hospitalization_part2()
        self.validate_hospitalization_part3()
        self.validate_clinic()

        return cleaned_data

    def validate_medical_care(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('medical_care') == NO:
            if cleaned_data.get('no_medical_care') == NOT_APPLICABLE:
                raise forms.ValidationError(
                    {'no_medical_care':
                     ('Please provide a reason. ref: {}'.format(get_linenumber()))})
            elif cleaned_data.get('no_medical_care') == OTHER:
                if not cleaned_data.get('no_medical_care_other'):
                    raise forms.ValidationError(
                        {'no_medical_care_other':
                         ('This field is required. ref: {}'.format(get_linenumber()))})
            elif cleaned_data.get('no_medical_care') != OTHER:
                if cleaned_data.get('no_medical_care_other'):
                    raise forms.ValidationError(
                        {'no_medical_care_other':
                         ('This field is not required. ref: {}'.format(get_linenumber()))})
        elif cleaned_data.get('medical_care') == YES:
            if cleaned_data.get('no_medical_care') != NOT_APPLICABLE:
                raise forms.ValidationError(
                    {'no_medical_care':
                     ('Participant has not received any medical care, '
                      'please give reason why not. ref: {}'.format(get_linenumber()))})
        elif cleaned_data.get('medical_care') == DWTA:
            if cleaned_data.get('no_medical_care') != DWTA:
                raise forms.ValidationError(
                    {'no_medical_care':
                     ('Field should be \'Don\'t want to answer\'. ref: {}'.format(get_linenumber()))})
            elif cleaned_data.get('no_medical_care_other'):
                raise forms.ValidationError(
                    {'no_medical_care_other':
                     ('This field is not required. ref: {}'.format(get_linenumber()))})

    def validate_ever_taken(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('ever_taken_arv') == YES
                and cleaned_data.get('why_no_arv') != NOT_APPLICABLE):
            raise forms.ValidationError({
                'why_no_arv': 'This field is not applicable. ref: {}'.format(get_linenumber())})
        elif (cleaned_data.get('ever_taken_arv') == NO
              and cleaned_data.get('why_no_arv') == NOT_APPLICABLE):
            raise forms.ValidationError({
                'why_no_arv': 'Please provide a reason. ref: {}'.format(get_linenumber())})

    def validate_art_part1(self):
        """Validations for first part of section Antiretiroviral
        Therapy.
        """
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('on_arv') == YES
                and cleaned_data.get('arv_stop_date')):
            raise forms.ValidationError({
                'arv_stop_date':
                'This field is not required. ref: {}'.format(get_linenumber())})
        elif (cleaned_data.get('on_arv') == NO
              and not cleaned_data.get('arv_stop_date')):
            raise forms.ValidationError({
                'arv_stop_date':
                'This field is required. ref: {}'.format(get_linenumber())})
        elif (cleaned_data.get('arv_stop_date')
                and cleaned_data.get('arv_stop') == NOT_APPLICABLE):
            raise forms.ValidationError({
                'arv_stop':
                'This field is applicable. ref: {}'.format(get_linenumber())})
        elif (not cleaned_data.get('arv_stop_date')
              and cleaned_data.get('arv_stop') != NOT_APPLICABLE):
            raise forms.ValidationError({
                'arv_stop':
                'This field is not applicable. ref: {}'.format(get_linenumber())})
        elif (cleaned_data.get('ever_taken') == YES
                and cleaned_data.get('on_arv') == NO
                and not cleaned_data.get('arv_stop_date')):
            raise forms.ValidationError({
                'arv_stop':
                'Participant was on ART. This field is required. ref: {}'.format(get_linenumber())})
        elif (cleaned_data.get('ever_taken') == NO
              and cleaned_data.get('first_arv')):
            raise forms.ValidationError({
                'first_arv':
                'This field is not required. ref: {}'.format(get_linenumber())})
        elif (cleaned_data.get('arv_stop') == OTHER
                and not cleaned_data.get('arv_stop_other')):
            raise forms.ValidationError({
                'arv_stop_other':
                'This field is required. ref: {}'.format(get_linenumber())})
        elif (cleaned_data.get('arv_stop') != OTHER
              and cleaned_data.get('arv_stop_other')):
            raise forms.ValidationError({
                'arv_stop_other':
                'This field is not required. ref: {}'.format(get_linenumber())})
        elif (cleaned_data.get('arv_stop_date') and cleaned_data.get('first_arv')
                and cleaned_data.get('arv_stop_date') <= cleaned_data.get('first_arv')):
            raise forms.ValidationError({
                'arv_stop_date':
                'Date cannot be on or before {}. (See ART start date above)'.format(
                    cleaned_data.get('first_arv').strftime('%Y-%m-%d'))})

    def validate_art_regimen(self, m2m_field=None, field_other=None):
        cleaned_data = self.cleaned_data
        m2m_field = m2m_field or 'arvs'
        field_other = field_other or 'arv_other'
        if (cleaned_data.get('on_arv') == NO
                and cleaned_data.get(m2m_field)):
            raise forms.ValidationError({
                m2m_field:
                'This field is not required.'})
        elif cleaned_data.get('on_arv') == YES:
            if cleaned_data.get(m2m_field):
                if (cleaned_data.get(m2m_field).count() == 0):
                    raise forms.ValidationError({
                        m2m_field:
                        'This field is required. Please make a selection.'})
                elif (cleaned_data.get(m2m_field).count() > 0):
                    for obj in cleaned_data.get(m2m_field):
                        if obj.short_name == NOT_APPLICABLE:
                            raise forms.ValidationError({
                                m2m_field:
                                'Invalid selection. Cannot be not applicable.'})
                        elif obj.short_name == OTHER and not cleaned_data.get(field_other):
                            raise forms.ValidationError({
                                field_other:
                                'This field is required.'})
            elif not cleaned_data.get(m2m_field):
                raise forms.ValidationError({
                    m2m_field:
                    'This field is required. Please make a selection.'})

    def validate_prev_art_regimen(self):
        cleaned_data = self.cleaned_data
        self.validate_is_first_regimen()
        if cleaned_data.get('is_first_regimen') == NO:
            if not cleaned_data.get('prev_switch_date'):
                raise forms.ValidationError({
                    'prev_switch_date':
                    'This field is required.'})
            elif (cleaned_data.get('prev_switch_date') and cleaned_data.get('first_arv')
                  and cleaned_data.get('prev_switch_date') <= cleaned_data.get('first_arv')):
                raise forms.ValidationError({
                    'prev_switch_date':
                    'Date cannot be on or before {}. (See ART start date above)'.format(
                        cleaned_data.get('first_arv').strftime('%Y-%m-%d'))})
            else:
                self.validate_art_regimen('prev_arvs', 'prev_arv_other')
        elif cleaned_data.get('is_first_regimen') == YES:
            self.prev_art_regimen_not_required()

    def validate_is_first_regimen(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('on_arv') == YES
                and not cleaned_data.get('is_first_regimen')):
            raise forms.ValidationError({
                'is_first_regimen':
                'This field is required.'})
        elif cleaned_data.get('on_arv') == NO:
            if cleaned_data.get('is_first_regimen'):
                raise forms.ValidationError({
                    'is_first_regimen':
                    'This field is not required.'})
            elif not cleaned_data.get('is_first_regimen'):
                self.prev_art_regimen_not_required()

    def prev_art_regimen_not_required(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('prev_switch_date'):
            raise forms.ValidationError({
                'prev_switch_date':
                'This field is not required.'})
        elif cleaned_data.get('prev_arvs'):
            raise forms.ValidationError({
                'prev_arvs':
                'This field is not required.'})
        elif cleaned_data.get('prev_arv_other'):
            raise forms.ValidationError({
                'prev_arv_other':
                'This field is not required.'})

    def validate_adherence(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('on_arv') == YES:
            if cleaned_data.get('adherence_4_day') == NOT_APPLICABLE:
                raise forms.ValidationError({
                    'adherence_4_day':
                    'This field is applicable'})
            elif cleaned_data.get('adherence_4_wk') == NOT_APPLICABLE:
                raise forms.ValidationError({
                    'adherence_4_wk':
                    'This field is applicable'})
        elif cleaned_data.get('on_arv') == NO:
            if cleaned_data.get('adherence_4_day') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'adherence_4_day':
                    'This field is not applicable'})
            elif cleaned_data.get('adherence_4_wk') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'adherence_4_wk':
                    'This field is not applicable'})

    def validate_hospitalization_part1(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('hospitalized_art_start') == YES:
            if cleaned_data.get('ever_taken_arv') == NO:
                raise forms.ValidationError({
                    'hospitalized_art_start':
                    'This field is not applicable'})
            elif not cleaned_data.get('hospitalized_art_start_duration'):
                raise forms.ValidationError({
                    'hospitalized_art_start_duration':
                    'This field is required'})
            elif cleaned_data.get('hospitalized_art_start_reason') == NOT_APPLICABLE:
                raise forms.ValidationError({
                    'hospitalized_art_start_reason':
                    'This field is applicable'})
        elif cleaned_data.get('hospitalized_art_start') == NO:
            if cleaned_data.get('ever_taken_arv') == NO:
                raise forms.ValidationError({
                    'hospitalized_art_start':
                    'This field is not applicable'})
            elif cleaned_data.get('hospitalized_art_start_duration'):
                raise forms.ValidationError({
                    'hospitalized_art_start_duration':
                    'This field is not required'})
            elif cleaned_data.get('hospitalized_art_start_reason') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'hospitalized_art_start_reason':
                    'This field is not applicable'})
        elif cleaned_data.get('hospitalized_art_start') == NOT_APPLICABLE:
            if cleaned_data.get('ever_taken_arv') == YES:
                raise forms.ValidationError({
                    'hospitalized_art_start':
                    'This field is applicable'})
            elif cleaned_data.get('hospitalized_art_start_duration'):
                raise forms.ValidationError({
                    'hospitalized_art_start_duration':
                    'This field is not required'})
            elif cleaned_data.get('hospitalized_art_start_reason') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'hospitalized_art_start_reason':
                    'This field is not applicable'})

    def validate_hospitalization_part2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('hospitalized_art_start_reason'):
            if (cleaned_data.get('hospitalized_art_start_reason') == OTHER
                    and not cleaned_data.get('hospitalized_art_start_reason_other')):
                raise forms.ValidationError({
                    'hospitalized_art_start_reason_other':
                    'This field is required'})
            elif (cleaned_data.get('hospitalized_art_start_reason') != OTHER
                    and cleaned_data.get('hospitalized_art_start_reason_other')):
                raise forms.ValidationError({
                    'hospitalized_art_start_reason_other':
                    'This field is not required'})
            elif (cleaned_data.get('hospitalized_art_start_reason') == 'chronic_disease'
                    and not cleaned_data.get('chronic_disease')):
                raise forms.ValidationError({
                    'chronic_disease':
                    'This field is required'})
            elif (cleaned_data.get('hospitalized_art_start_reason') != 'chronic_disease'
                  and cleaned_data.get('chronic_disease')):
                raise forms.ValidationError({
                    'chronic_disease':
                    'This field is not required'})
            elif (cleaned_data.get('hospitalized_art_start_reason') == 'medication_toxicity'
                  and not cleaned_data.get('medication_toxicity')):
                raise forms.ValidationError({
                    'medication_toxicity':
                    'This field is required'})
            elif (cleaned_data.get('hospitalized_art_start_reason') != 'medication_toxicity'
                  and cleaned_data.get('medication_toxicity')):
                raise forms.ValidationError({
                    'medication_toxicity':
                    'This field is not required'})
        elif not cleaned_data.get('hospitalized_art_start_reason'):
            if cleaned_data.get('chronic_disease'):
                raise forms.ValidationError({
                    'chronic_disease':
                    'This field is not required'})
            elif cleaned_data.get('medication_toxicity'):
                raise forms.ValidationError({
                    'medication_toxicity':
                    'This field is not required'})

    def validate_hospitalization_part3(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('hospitalized_art_start') == YES:
            if not cleaned_data.get('hospitalized_evidence'):
                raise forms.ValidationError({
                    'hospitalized_evidence':
                    'This field is required'})
            elif (cleaned_data.get('hospitalized_evidence') == OTHER
                  and not cleaned_data.get('hospitalized_evidence_other')):
                raise forms.ValidationError({
                    'hospitalized_evidence_other':
                    'This field is required'})
            elif (cleaned_data.get('hospitalized_evidence') != OTHER
                  and cleaned_data.get('hospitalized_evidence_other')):
                raise forms.ValidationError({
                    'hospitalized_evidence_other':
                    'This field is not required'})
        elif cleaned_data.get('hospitalized_art_start') == NO:
            if cleaned_data.get('hospitalized_evidence'):
                raise forms.ValidationError({
                    'hospitalized_evidence':
                    'This field is not required'})

    def validate_clinic(self):
        cleaned_data = self.cleaned_data
        if (cleaned_data.get('on_arv') == YES
                and not cleaned_data.get('clinic_receiving_from')):
            raise forms.ValidationError({
                'clinic_receiving_from':
                'This field is required'})
        elif (cleaned_data.get('on_arv') == NO
              and cleaned_data.get('clinic_receiving_from')):
            raise forms.ValidationError({
                'clinic_receiving_from':
                'This field is not required'})
        elif (cleaned_data.get('clinic_receiving_from')
              and not cleaned_data.get('next_appointment_date')):
            raise forms.ValidationError({
                'next_appointment_date':
                'This field is required'})
        elif (not cleaned_data.get('clinic_receiving_from')
              and cleaned_data.get('next_appointment_date')):
            raise forms.ValidationError({
                'next_appointment_date':
                'This field is not required'})

    class Meta:
        model = HivCareAdherence
        fields = '__all__'
