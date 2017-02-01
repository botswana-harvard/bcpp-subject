from django import forms

from edc_consent.modelform_mixins import RequiresConsentModelFormMixin

from ..models import SubjectVisit
from edc_consent.site_consents import site_consents
from bcpp.consents import ANONYMOUS_CONSENT_GROUP
from edc_base.modelform_mixins import CommonCleanModelFormMixin


class SubjectVisitForm (RequiresConsentModelFormMixin,
                        CommonCleanModelFormMixin, forms.ModelForm):

    def get_consent(self, subject_identifier, report_datetime):
        """Return an instance of the consent model.
        """
        cleaned_data = self.cleaned_data
        if cleaned_data.get('household_member').anonymous:
            consent_object = site_consents.get_consent(
                report_datetime=report_datetime,
                consent_group=ANONYMOUS_CONSENT_GROUP,
                consent_model=self._meta.model._meta.anonymous_consent_model)
        else:
            consent_object = site_consents.get_consent(
                report_datetime=report_datetime,
                consent_group=self._meta.model._meta.consent_group,
                consent_model=self._meta.model._meta.consent_model)
        try:
            obj = consent_object.model.consent.consent_for_period(
                subject_identifier=subject_identifier,
                report_datetime=report_datetime)
        except consent_object.model.DoesNotExist:
            raise forms.ValidationError(
                '\'{}\' does not exist to cover this subject on {}.'.format(
                    consent_object.model._meta.verbose_name,
                    report_datetime=report_datetime.strftime('Y%-%m-%d %Z')))
        return obj

    class Meta:
        model = SubjectVisit
        fields = '__all__'
