from edc_dashboard.view_mixins import ConsentViewMixin as BaseConsentViewMixin

from ...models.utils import get_enrollment_survey


class ConsentViewMixin(BaseConsentViewMixin):

    @property
    def empty_consent(self):
        return self.consent_model(
            subject_identifier=self.subject_identifier,
            household_member=self.household_member._original_object,
            survey=get_enrollment_survey(
                [obj for obj in self.consents if obj.id], self.survey_schedule_object),
            survey_schedule=self.survey_schedule_object.field_value,
            version=self.consent_object.version)
