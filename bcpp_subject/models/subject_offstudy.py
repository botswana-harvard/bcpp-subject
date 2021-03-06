from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_offstudy.model_mixins import OffstudyModelMixin, OffstudyModelManager


class SubjectOffstudy(OffstudyModelMixin, BaseUuidModel):

    """A model completed by the user that completed when the subject is taken off-study."""

    objects = OffstudyModelManager()

    history = HistoricalRecords()

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Subject Off Study"
        verbose_name_plural = "Subject Off Study"
