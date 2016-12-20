from django.db import models

from survey.model_mixins import SurveyModelMixin as ParentSurveyModelMixin


class SurveyModelMixin(ParentSurveyModelMixin, models.Model):

    def save(self, *args, **kwargs):
        if not self.id:
            self.survey = self.household_member.household_structure.survey
        super().save(*args, **kwargs)
