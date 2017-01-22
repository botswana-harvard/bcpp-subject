from edc_base.utils import get_utcnow
from edc_constants.constants import MALE
from edc_visit_schedule.site_visit_schedules import site_visit_schedules


class EnrollmentFormsViewMixin:

    @property
    def enrollment_forms(self):
        """Returns a generator of enrollment instances for this subject."""
        for visit_schedule in site_visit_schedules.get_visit_schedules().values():
            for schedule in visit_schedule.schedules.values():
                obj = schedule.enrollment_instance(
                    subject_identifier=self.subject_identifier)
                if obj:
                    yield obj
                else:
                    continue

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            MALE=MALE,
            reference_datetime=get_utcnow(),
            enrollment_forms=self.enrollment_forms,
        )
        return context
