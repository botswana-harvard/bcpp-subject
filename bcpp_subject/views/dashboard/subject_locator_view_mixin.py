from ...models.subject_locator import SubjectLocator

from ..wrappers import SubjectLocatorModelWrapper


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
            subject_locator = SubjectLocator(subject_identifier=self.subject_identifier)
        self.subject_locator = self.subject_locator_model_wrapper_class(subject_locator)
        kwargs['subject_locator'] = self.subject_locator
        return super().get(request, *args, **kwargs)
