import arrow

from django import forms

from edc_base.modelform_mixins import (
    CommonCleanModelFormMixin, JSONModelFormMixin)
from edc_base.modelform_validators import (
    OtherSpecifyFieldValidator, ManyToManyFieldValidator,
    ApplicableFieldValidator, RequiredFieldValidator)
from edc_constants.constants import NO, DWTA, YES

from ..constants import DAYS, MONTHS, YEARS
from ..models import SubjectVisit, PartnerResidency, SexualBehaviour, HivTestingHistory


class SubjectModelFormMixin(CommonCleanModelFormMixin,
                            OtherSpecifyFieldValidator,
                            ApplicableFieldValidator,
                            ManyToManyFieldValidator,
                            RequiredFieldValidator,
                            JSONModelFormMixin,
                            forms.ModelForm):

    visit_model = SubjectVisit


class PreviousAppointmentFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._previous_appointment_rdate = None
        self._previous_appointment = None

    @property
    def previous_appointment(self):
        if not self._previous_appointment:
            cleaned_data = self.cleaned_data
            self._previous_appointment = cleaned_data.get(
                'subject_visit').appointment.previous_by_timepoint
        return self._previous_appointment

    @property
    def previous_appointment_rdate(self):
        """Returns the utc arrow object of appt_datetime of the previous
        appointment

        Usage:
            from django.conf import settings
            rdate.to(settings.TIME_ZONE).date()
            rdate.to(settings.TIME_ZONE).datetime
        """
        if not self._previous_appointment_rdate:
            if self.previous_appointment:
                rdate = arrow.Arrow.fromdatetime(
                    self.previous_appointment.appt_datetime,
                    tzinfo=self.previous_appointment.appt_datetime.tzinfo)
            else:
                rdate = None
            self._previous_appointment_rdate = rdate
        return self._previous_appointment_rdate


class HivTestFormMixin:

    def clean(self):
        cleaned_data = super().clean()
        self.validate_hiv_test_review_complete()
        return cleaned_data

    def validate_hiv_test_review_complete(self):
        cleaned_data = self.cleaned_data
        try:
            HivTestingHistory.objects.get(
                subject_visit=cleaned_data.get('subject_visit'))
        except HivTestingHistory.DoesNotExist:
            raise forms.ValidationError(
                'Please complete {} first.'.format(
                    HivTestingHistory._meta.verbose_name))


class SexualPartnerFormMixin:

    def clean(self):
        cleaned_data = super().clean()
        try:
            subject_behaviour = SexualBehaviour.objects.get(
                subject_visit=cleaned_data.get('subject_visit'))
        except SexualBehaviour.DoesNotExist:
            raise forms.ValidationError(
                'Please complete {} first.'.format(
                    SexualBehaviour._meta.verbose_name))
        else:
            if subject_behaviour.lifetime_sex_partners == 1:
                if cleaned_data.get('concurrent') not in [NO, DWTA]:
                    raise forms.ValidationError({
                        'concurrent': (
                            "You wrote that you have only one partner ever on {}. "
                            "Please correct if you have sex with other partners.".format(
                                SexualBehaviour._meta.verbose_name))})

        responses = []
        for obj in PartnerResidency.objects.all():
            if ('outside' in obj.short_name.lower()
                    and 'community' in obj.short_name.lower()):
                responses.append(obj.short_name)
        self.m2m_other_specify_applicable(
            *responses,
            m2m_field='first_partner_live',
            field_other='sex_partner_community')

        self.required_if(
            DAYS, MONTHS, field='third_last_sex', field_required='third_last_sex_calc')
        self.required_if(
            DAYS, MONTHS, YEARS, field='first_first_sex', field_required='first_first_sex_calc')
        self.validate_other_specify('first_relationship')
        self.validate_other_specify(
            'first_exchange_age', other_stored_value='gte_19')

#         if (cleaned_data.get('first_partner_hiv') == 'negative'
#                 and cleaned_data.get('first_haart') in self.yes_no_unsure_options):
#             raise forms.ValidationError(
#                 'Do not answer this question if partners HIV status is '
#                 'known to be negative')
#
#         if (cleaned_data.get('first_partner_hiv') == 'I am not sure'
#                 and cleaned_data.get('first_haart') in self.yes_no_unsure_options):
#             raise forms.ValidationError(
#                 'If partner status is not known, do not give information '
#                 'about status of ARV\'s')
        return cleaned_data


class MobileTestModelFormMixin:

    def clean(self):
        cleaned_data = super().clean()
        self.required_if(
            NO, field='test_done', field_required='reason_not_done')
        self.validate_other_specify('reason_not_done')
        self.required_if(
            YES, field='test_done', field_required='machine_identifier')
        self.required_if(YES, field='test_done', field_required='result_value')
        self.required_if(
            YES, field='test_done', field_required='result_datetime')
        return cleaned_data
