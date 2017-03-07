from uuid import uuid4

from edc_dashboard.view_mixins import ConsentViewMixin as BaseConsentViewMixin


class ConsentViewMixin(BaseConsentViewMixin):

    @property
    def empty_consent(self):
        """Returns a new unsaved mock consent model.
        """
        return self.consent_model(
            consent_identifier=str(uuid4()),
            household_member=self.household_member,
            survey_schedule=self.household_member.survey_schedule_object.field_value,
            version=self.consent_object.version)
