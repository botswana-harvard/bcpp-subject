from django.db import models

from edc_base.model_managers import HistoricalRecords

from .model_mixins import CrfModelMixin, CrfModelManager, SexualPartnerMixin


class ThirdPartner (SexualPartnerMixin, CrfModelMixin):
    """A model completed by the user on the participant's
    recent sexual behaviour.
    """

    third_partner_arm = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    objects = CrfModelManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.third_partner_arm = self.get_partner_arm()
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = 'Third Partner - 12 Months'
        verbose_name_plural = 'Third Partners - 12 Months'
