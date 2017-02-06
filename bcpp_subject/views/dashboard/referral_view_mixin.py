from ...referral.referral import Referral
from pprint import pprint


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
            pprint(self.referral.__dict__)
            print(self.referral.referral_code)
        kwargs['referral'] = self.referral
        return super().get(request, *args, **kwargs)
