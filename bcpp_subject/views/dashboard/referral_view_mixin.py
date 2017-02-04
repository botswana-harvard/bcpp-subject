from ...referral.referral import Referral
from ...models import SubjectReferral


class ReferralViewMixin:

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.referral = None

    def get(self, request, *args, **kwargs):
        try:
            subject_visit = self.appointment.visit._original_object
        except AttributeError:
            pass
        else:
            try:
                subject_referral = SubjectReferral.objects.get(
                    subject_visit=subject_visit)
            except SubjectReferral.DoesNotExist:
                pass
            else:
                self.referral = Referral(subject_referral)
        kwargs['referral'] = self.referral
        return super().get(request, *args, **kwargs)
