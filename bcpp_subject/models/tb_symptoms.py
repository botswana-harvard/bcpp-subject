from django.db import models

from edc_base.model_managers import HistoricalRecords
from edc_constants.constants import YES

from .model_mixins import CrfModelMixin
from ..models.model_mixins.crf_model_mixin import CrfModelManager
from edc_constants.choices import YES_NO


class TbSymtomsManager(CrfModelManager):

    def get_symptoms(self, subject_visit):
        symptoms = []
        try:
            obj = self.get(subject_visit=subject_visit)
            if obj.cough == YES:
                symptoms.append('cough')
            if obj.lymph_nodes == YES:
                symptoms.append('lymph_nodes')
            if obj.night_sweat == YES:
                symptoms.append('night_sweat')
            if obj.cough_blood == YES:
                symptoms.append('cough_blood')
            if obj.weight_loss == YES:
                symptoms.append('weight_loss')
            symptoms.sort()
        except self.model.DoesNotExist:
            pass
        return ', '.join(symptoms)


class TbSymptoms (CrfModelMixin):

    """
    A user form to capture basic TB symptoms.

    This data is not collected for a formal referral. RA may do
    an informal verbal referral.

    """
    cough = models.CharField(
        verbose_name=(
            "Does the participant currently have a COUGH that "
            "has lasted for more than 2 weeks?"),
        max_length=10,
        choices=YES_NO,
        help_text="",
    )

    fever = models.CharField(
        verbose_name="In the last two weeks has the participant had FEVER?",
        max_length=10,
        choices=YES_NO,
        help_text="",
    )

    lymph_nodes = models.CharField(
        verbose_name="Does the participant currently have ENLARGED LYMPH NODES?",
        max_length=10,
        choices=YES_NO,
        help_text="",
    )

    cough_blood = models.CharField(
        verbose_name="In the last two weeks has the participant COUGHED UP BLOOD?",
        max_length=10,
        choices=YES_NO,
        help_text="",
    )

    night_sweat = models.CharField(
        verbose_name="In the last two weeks has the participant had NIGHT SWEATS?",
        max_length=10,
        choices=YES_NO,
        help_text="",
    )

    weight_loss = models.CharField(
        verbose_name="In the last month has the participant had unexplained WEIGHT LOSS?",
        max_length=10,
        choices=YES_NO,
        help_text="",
    )

    objects = TbSymtomsManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "TB Symptoms"
        verbose_name_plural = "TB Symptoms"
