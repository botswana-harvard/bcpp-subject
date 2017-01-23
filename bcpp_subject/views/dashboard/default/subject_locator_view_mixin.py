from ....models import SubjectLocator

from ...wrappers import SubjectLocatorModelWrapper


class SubjectLocatorViewMixin:

    subject_locator_model_wrapper_class = SubjectLocatorModelWrapper

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subject_locator = None

    def get(self, request, *args, **kwargs):
        try:
            subject_locator = SubjectLocator.objects.get(
                subject_identifier=self.subject_identifier)
        except SubjectLocator.DoesNotExist:
            subject_locator = SubjectLocator(
                subject_identifier=self.subject_identifier)
        self.subject_locator = self.subject_locator_model_wrapper_class(
            subject_locator,
            household_identifier=self.household_identifier,
            survey_schedule=self.survey_schedule_object.field_value)
        kwargs['subject_locator'] = self.subject_locator
        print(self.subject_locator._original_object)
        return super().get(request, *args, **kwargs)
