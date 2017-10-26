from edc_appointment.appointment_creator import AppointmentCreator


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
    def extra_create_appointment_options(self):
        """User can add extra options for appointment.objects.create.
        """
        options = dict(
            survey=self.model_obj.survey_object.field_value,
            survey_schedule=self.model_obj.survey_schedule_object.field_value,
            household_member=self.model_obj.get_household_member)
        return options
