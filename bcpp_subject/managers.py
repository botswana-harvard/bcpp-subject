from django.db import models


class DisenrollmentManager(models.Manager):

    def get_by_natural_key(self, subject_identifier, visit_schedule_name, schedule_name):
        return self.get(
            subject_identifier=subject_identifier,
            visit_schedule_name=visit_schedule_name, schedule_name=schedule_name)


class EnrollmentManager(models.Manager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        return self.get(subject_identifier=subject_identifier_as_pk)
