from bcpp_status.status_helper import StatusHelper

from edc_constants.constants import UNK


class StatusHelperViewMixin:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.status_helper = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.subject_visit:
            self.status_helper = StatusHelper(visit=self.subject_visit)
        context.update(
            status_helper=self.status_helper,
            UNK=UNK)
        return context
