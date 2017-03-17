from edc_base.model_managers import HistoricalRecords

from .model_mixins import CrfModelMixin, MobileTestModelMixin


class PimaCd4(MobileTestModelMixin, CrfModelMixin):

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = 'PIMA CD4 count'
        verbose_name_plural = 'PIMA CD4 count'
