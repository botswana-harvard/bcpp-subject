from django.db import models


class DisenrollmentManager(models.Manager):

    def get_by_natural_key(self, subject_identifier, visit_schedule_name, schedule_name):
        return self.get(
            subject_identifier=subject_identifier,
            visit_schedule_name=visit_schedule_name, schedule_name=schedule_name)


class EnrollmentManager(models.Manager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        return self.get(subject_identifier=subject_identifier_as_pk)


class SubjectConsentManager(models.Manager):

    def get_by_natural_key(
            self, subject_identifier, version, internal_identifier, survey, household_identifier, plot_identifier):
        return self.get(
            subject_identifier=subject_identifier, version=version,
            household_member__internal_identifier=internal_identifier,
            household_member__household_structure__survey=survey,
            household_member__household_structure__household_identifier=household_identifier,
            household_member__household_structure__household__plot__plot_identifier=plot_identifier
        )


class CorrectConsentManager(models.Manager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        return self.get(subject_identifier=subject_identifier_as_pk)
