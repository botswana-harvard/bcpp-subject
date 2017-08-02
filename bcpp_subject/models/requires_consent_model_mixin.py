from django.conf import settings
from django.db.models import options

from edc_consent.model_mixins import RequiresConsentMixin as BaseRequiresConsentMixin
from edc_consent.site_consents import site_consents

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('anonymous_consent_model',)


class RequiresConsentMixin(BaseRequiresConsentMixin):

    def get_consent_object(self):
        try:
            household_member = self.subject_visit.household_member
        except AttributeError:
            household_member = self.household_member
        if household_member.anonymous:
            consent_object = site_consents.get_consent(
                consent_model=self._meta.anonymous_consent_model,
                consent_group=settings.ANONYMOUS_CONSENT_GROUP,
                report_datetime=self.report_datetime)
        else:
            consent_object = site_consents.get_consent(
                consent_model=self._meta.consent_model,
                report_datetime=self.report_datetime)
        return consent_object

    class Meta(BaseRequiresConsentMixin.Meta):
        abstract = True
        consent_model = None
        anonymous_consent_model = None
