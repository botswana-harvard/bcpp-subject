from edc_constants.constants import UNK

from bcpp_subject.subject_helper import SubjectHelper


class SubjectHelperViewMixin:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subject_helper = None

    def get(self, request, *args, **kwargs):
        try:
            subject_visit = self.appointment.visit._original_object
        except AttributeError as e:
            print(e)
            self.subject_helper = None
        else:
            self.subject_helper = SubjectHelper(subject_visit)
        kwargs['subject_helper'] = self.subject_helper
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(UNK=UNK)
        return context
