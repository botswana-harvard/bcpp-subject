from bcpp_status.status_helper import StatusHelper

from edc_constants.constants import UNK


class SubjectHelperViewMixin:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subject_helper = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.subject_visit:
            self.subject_helper = StatusHelper(visit=self.subject_visit)
        context.update(
            subject_helper=self.subject_helper,
            UNK=UNK)
        return context
