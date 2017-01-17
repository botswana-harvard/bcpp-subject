from edc_dashboard.view_mixins import ConsentViewMixin as BaseConsentViewMixin


class ConsentViewMixin(BaseConsentViewMixin):

    @property
    def empty_consent(self):
        return self.consent_model(
            subject_identifier=self.subject_identifier,
            household_member=self.household_member._original_object,
            version=self.consent_object.version)
