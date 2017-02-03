from datetime import date
from inspect import currentframe

from django import forms

from edc_constants.constants import YES, NO, OTHER, NOT_APPLICABLE, DWTA

from ..models import HivCareAdherence
from .form_mixins import SubjectModelFormMixin


def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno


class HivCareAdherenceForm(SubjectModelFormMixin):

    def validate_art_regimen(self):
        cleaned_data = self.cleaned_data

        if cleaned_data.get('on_arv') == NO:
            if cleaned_data.get('regimen_currently_prescribed'):
                if (cleaned_data.get('regimen_currently_prescribed').count() != 1):
                    raise forms.ValidationError({
                        'regimen_currently_prescribed':
                        'Invalid selection. Expected not applicable only.'})
                elif (cleaned_data.get('regimen_currently_prescribed').count() == 1):
                    if cleaned_data.get('regimen_currently_prescribed')[0].short_name != NOT_APPLICABLE:
                        raise forms.ValidationError({
                            'regimen_currently_prescribed':
                            'Invalid selection. Expected not applicable.'})
        elif cleaned_data.get('on_arv') == YES:
            if cleaned_data.get('regimen_currently_prescribed'):
                if (cleaned_data.get('regimen_currently_prescribed').count() == 0):
                    raise forms.ValidationError({
                        'regimen_currently_prescribed':
                        'This field is required. Please make a selection.'})
                elif (cleaned_data.get('regimen_currently_prescribed').count() != 0):
                    if (NOT_APPLICABLE in [
                            obj.short_name for obj in cleaned_data.get(
                                'regimen_currently_prescribed')]):
                        raise forms.ValidationError({
                            'regimen_currently_prescribed':
                            'Invalid selection. Cannot be not applicable.'})

        # if cleaned_data('regimen_currently_prescribed'):

    def clean(self):
        cleaned_data = super().clean()

        # section: care
        self.validate_medical_care()
        self.validate_ever_taken()
        self.validate_art_part1()
        self.validate_art_regimen()

        # self.validate_ever_taken_arv()
        # self.validate_choose_chronic_infection()

        # Care
        if cleaned_data.get('ever_taken_arv') == NO:
            if cleaned_data.get('arv_stop'):
                raise forms.ValidationError({
                    'arv_stop':
                    'Participant has never taken ART. '
                    'This field is not required.'})
            if cleaned_data.get('on_arv') == YES:
                raise forms.ValidationError({
                    'on_arv':
                    'Participant has never taken ART. '
                    'This field is not required.'})

        self.validate_on_arv()
        self.validate_not_on_arv()

        if (cleaned_data.get('arv_stop') == OTHER and not
                cleaned_data.get('arv_stop_other')):
            raise forms.ValidationError({
                'arv_stop_other':
                'If participant reason for stopping ARV\'s is \'OTHER\', '
                'specify reason why stopped taking ARV\'s?'})
        if cleaned_data.get('first_positive'):
            if cleaned_data.get('first_positive') == date.today():
                raise forms.ValidationError({
                    'first_positive':
                    'Date first received HIV positive result CANNOT be '
                    'today. Please correct.'})
        if cleaned_data.get('next_appointment_date'):
            if not cleaned_data.get('next_appointment_date') >= date.today():
                raise forms.ValidationError({
                    'next_appointment_date':
                    'The next appointment date must be on or '
                    'after the report datetime. You entered '
                    '{0}.'.format(cleaned_data.get(
                        'next_appointment_date').strftime('%Y-%m-%d'))})

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
            if cleaned_data.get('no_medical_care_other'):
                raise forms.ValidationError(
                    {'no_medical_care_other':
                     ('This field is not required. ref: {}'.format(get_linenumber()))})

    def validate_ever_taken(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('ever_taken_arv') == YES:
            if cleaned_data.get('why_no_arv') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'why_no_arv': 'This field is not applicable. ref: {}'.format(get_linenumber())})
        elif cleaned_data.get('ever_taken_arv') == NO:
            if cleaned_data.get('why_no_arv') == NOT_APPLICABLE:
                raise forms.ValidationError({
                    'why_no_arv': 'Please provide a reason. ref: {}'.format(get_linenumber())})
        elif cleaned_data.get('ever_taken_arv') == DWTA:
            if cleaned_data.get('why_no_arv') != DWTA:
                raise forms.ValidationError({
                    'why_no_arv':
                    'Field should be \'Don\'t want to answer\'. ref: {}'.format(get_linenumber())})

    def validate_art_part1(self):
        """Validations for first part of section Antiretiroviral
        Therapy.
        """
        cleaned_data = self.cleaned_data
        if cleaned_data.get('on_arv') == YES:
            if cleaned_data.get('arv_stop_date'):
                raise forms.ValidationError({
                    'arv_stop_date':
                    'This field is not required. ref: {}'.format(get_linenumber())})
        elif cleaned_data.get('on_arv') == NO:
            if not cleaned_data.get('arv_stop_date'):
                raise forms.ValidationError({
                    'arv_stop_date':
                    'This field is required. ref: {}'.format(get_linenumber())})

        if cleaned_data.get('arv_stop_date'):
            if cleaned_data.get('arv_stop') == NOT_APPLICABLE:
                raise forms.ValidationError({
                    'arv_stop':
                    'This field is applicable. ref: {}'.format(get_linenumber())})
        elif not cleaned_data.get('arv_stop_date'):
            if cleaned_data.get('arv_stop') != NOT_APPLICABLE:
                raise forms.ValidationError({
                    'arv_stop':
                    'This field is not applicable. ref: {}'.format(get_linenumber())})

        if cleaned_data.get('ever_taken') == YES:
            if (cleaned_data.get('on_arv') == NO
                    and not cleaned_data.get('arv_stop_date')):
                raise forms.ValidationError({
                    'arv_stop':
                    'Participant was on ART. This field is required. ref: {}'.format(get_linenumber())})
        elif cleaned_data.get('ever_taken') == NO:
            if cleaned_data.get('first_arv'):
                raise forms.ValidationError({
                    'first_arv':
                    'This field is not required. ref: {}'.format(get_linenumber())})

        if cleaned_data.get('arv_stop') == OTHER:
            if not cleaned_data.get('arv_stop_other'):
                raise forms.ValidationError({
                    'arv_stop_other':
                    'This field is required. ref: {}'.format(get_linenumber())})
        elif cleaned_data.get('arv_stop') != OTHER:
            if cleaned_data.get('arv_stop_other'):
                raise forms.ValidationError({
                    'arv_stop_other':
                    'This field is not required. ref: {}'.format(get_linenumber())})

    def validate_ever_taken_arv(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('ever_taken_arv') == YES:
            if (cleaned_data.get('on_arv') == NO and not
                    cleaned_data.get('arv_stop_date')):
                raise forms.ValidationError({
                    'arv_stop_date':
                    'Participant has taken ART but stopped. '
                    'This field is required.'})
            if not cleaned_data.get('first_arv'):
                raise forms.ValidationError({
                    'first_arv':
                    'Participant has taken ART. This field is required.'})
            if cleaned_data.get('why_no_arv'):
                raise forms.ValidationError({
                    'why_no_arv':
                    'Participant has taken ART. This field is not required.'})

    def validate_on_arv(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('on_arv') == YES:
            if not cleaned_data.get('adherence_4_day'):
                raise forms.ValidationError({
                    'adherence_4_day':
                    'Participant is on ART. This field is required'})
            if not cleaned_data.get('clinic_receiving_from'):
                raise forms.ValidationError({
                    'clinic_receiving_from':
                    'Participant is on ART. This field is required'})
            if not cleaned_data.get('next_appointment_date'):
                raise forms.ValidationError({
                    'next_appointment_date':
                    'Participant is on ART. This field is required'})
            if cleaned_data.get('arv_stop_date'):
                raise forms.ValidationError({
                    'arv_stop_date':
                    'Participant is on ART. This field is not required'})
            if cleaned_data.get('arv_stop'):
                raise forms.ValidationError({
                    'arv_stop':
                    'Participant is on ART. This field is not required'})
            if not cleaned_data.get('arv_evidence'):
                raise forms.ValidationError({
                    'arv_evidence':
                    'Participant is on ART. This field is required'})

    def validate_not_on_arv(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('on_arv') == NO:
            if cleaned_data.get('adherence_4_wk'):
                raise forms.ValidationError({
                    'adherence_4_wk':
                    'Participant is not on ART. This field is not required'})
            if cleaned_data.get('adherence_4_day'):
                raise forms.ValidationError({
                    'adherence_4_day':
                    'Participant is not on ART. This field is not required'})
            if cleaned_data.get('clinic_receiving_from'):
                raise forms.ValidationError({
                    'clinic_receiving_from':
                    'Participant is not on ART. This field is not required'})
            if cleaned_data.get('next_appointment_date'):
                raise forms.ValidationError({
                    'next_appointment_date':
                    'Participant is not on ART. This field is not required'})
            if cleaned_data.get('arv_stop_date'):
                raise forms.ValidationError({
                    'arv_stop_date':
                    'Participant is not on ART. This field is not required'})
            if cleaned_data.get('arv_stop_other'):
                raise forms.ValidationError({
                    'arv_stop_other':
                    'Participant is not on ART. This field is not required'})
            if cleaned_data.get('arv_stop'):
                raise forms.ValidationError({
                    'arv_stop':
                    'Participant is not on ART. This field is not required'})

    def validate_choose_chronic_infection(self):
        cleaned_data = self.cleaned_data
        hospitalised_reasons = cleaned_data.get(
            'hospitalized_art_start_reason')
        if hospitalised_reasons and hospitalised_reasons.count() != 0:
            if any(hospitalised_reason == 'Chronic disease related care'
                   for hospitalised_reason in hospitalised_reasons):
                raise forms.ValidationError({
                    'hospitalized_art_start_reason':
                    'Participant choose chronic disease. Answer next question'})

    class Meta:
        model = HivCareAdherence
        fields = '__all__'
