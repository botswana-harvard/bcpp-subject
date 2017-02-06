from ...referral.referral import Referral


class ReferralViewMixin:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.referral = None

    def get(self, request, *args, **kwargs):
        try:
            subject_visit = self.appointment._original_object.subjectvisit
        except AttributeError:
            pass
        else:
            self.referral = Referral(subject_visit)
        kwargs['referral'] = self.referral
        return super().get(request, *args, **kwargs)
