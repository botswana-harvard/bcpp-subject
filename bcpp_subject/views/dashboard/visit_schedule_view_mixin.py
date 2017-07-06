from edc_visit_schedule.view_mixins import VisitScheduleViewMixin as BaseVisitScheduleViewMixin


class VisitScheduleViewMixin(BaseVisitScheduleViewMixin):

    def is_current_enrollment_model(self, enrollment_instance,
                                    schedule=None, **kwargs):
        if (enrollment_instance.survey_schedule_object.field_value ==
                self.survey_schedule_object.field_value):
            return True
        return False
