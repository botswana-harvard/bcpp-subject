from edc_dashboard.view_mixins import ConsentViewMixin as BaseConsentViewMixin
from edc_base.utils import get_uuid


class ConsentViewMixin(BaseConsentViewMixin):

    @property
    def empty_consent(self):
        """Returns a new unsaved mock consent model.
        """
        return self.consent_model(
            consent_identifier=get_uuid(),
            household_member=self.household_member,
            survey_schedule=self.household_member.survey_schedule_object.field_value,
            version=self.consent_object.version)
