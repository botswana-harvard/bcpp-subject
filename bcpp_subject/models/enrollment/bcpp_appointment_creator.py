from edc_appointment.appointment_creator import AppointmentCreator
from bcpp_community.surveys import BCPP_YEAR_1, BCPP_YEAR_2, BCPP_YEAR_3


class BcppAppointmentCreator(AppointmentCreator):

    @property
    def options(self):
        options = super().options
        options.update(
            survey=self.model_obj.survey_object.field_value,
            survey_schedule=self.model_obj.survey_schedule_object.field_value,
            household_member=self.model_obj.household_member)
        return options


class BcppAhsAppointmentCreator(AppointmentCreator):

    @property
    def options(self):
        """User can add extra options for appointment.objects.create.
        """
        options = super().options
        visit_code = options.get('visit_code')
        household_member = self.model_obj.get_household_member(
            visit_code=visit_code)
        map_area = household_member.household_structure.household.plot.map_area
        survey_schedule_items = household_member.survey_schedule.split('.')
        if BCPP_YEAR_1 in survey_schedule_items:
            survey = f'bcpp-survey.bcpp-year-1.ahs.{map_area}'
        elif BCPP_YEAR_2 in survey_schedule_items:
            survey = f'bcpp-survey.bcpp-year-2.ahs.{map_area}'
        elif BCPP_YEAR_3 in survey_schedule_items:
            survey = f'bcpp-survey.bcpp-year-3.ahs.{map_area}'
        options.update(
            survey=self.model_obj.get_survey_object(survey=survey).field_value,
            survey_schedule=household_member.survey_schedule,
            household_member=household_member)
        return options
