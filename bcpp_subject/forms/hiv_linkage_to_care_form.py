from django import forms

from edc_constants.constants import YES, NO

from ..models import HivLinkageToCare, HivCareAdherence
from .form_mixins import SubjectModelFormMixin


class HivLinkageToCareForm (SubjectModelFormMixin):

    def clean(self):
        cleaned_data = super().clean()
        try:
            HivCareAdherence.objects.get(
                subject_visit=cleaned_data.get('subject_visit'))
        except HivCareAdherence.DoesNotExist:
            raise forms.ValidationError(
                'Please complete {} first.'.format(
                    HivCareAdherence._meta.verbose_name))

        self.required_if_true(
            (cleaned_data.get('kept_appt') == 'attended_different_clinic'
             or cleaned_data.get('kept_appt') == 'went_different_clinic'),
            field_required='different_clinic')

        self.required_if(
            'failed_attempt', field='kept_appt', field_required='failed_attempt_date')

        self.validate_other_specify('evidence_referral')

        self.required_if(
            YES, field='recommended_art', field_required='reason_recommended_art')

        self.validate_other_specify('reason_recommended_art')

        self.required_if(
            YES, field='initiated', field_required='initiated_date')

        self.validate_other_specify('evidence_art')

        return cleaned_data

    class Meta:
        model = HivLinkageToCare
        fields = '__all__'
