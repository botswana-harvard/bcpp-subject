from django.db import models

from edc_base.model.fields import OtherCharField
from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO_UNSURE, YES_NO

from ..choices import COMMUNITY_NA
from ..exceptions import CircumcisionError

from .model_mixins import CrfModelMixin, CrfModelManager, CircumcisionModelMixin


class Circumcision (CircumcisionModelMixin, CrfModelMixin):

    circumcised = models.CharField(
        verbose_name="Are you circumcised?",
        max_length=15,
        choices=YES_NO_UNSURE,
        help_text="")

    last_seen_circumcised = models.CharField(
        verbose_name="Since we last spoke with you on last_seen_circumcised, have you been circumcised?",
        max_length=15,
        null=True,
        blank=True,
        choices=YES_NO,
        help_text="")

    circumcised_datetime = models.DateField(
        verbose_name='If Yes, date?',
        default=None,
        null=True,
        blank=True,
        help_text=""
    )

    circumcised_location = models.CharField(
        verbose_name="IF YES, Location?",
        max_length=25,
        choices=COMMUNITY_NA,
        null=True,
        blank=True,
        help_text="")

    circumcised_location_other = OtherCharField()

    objects = CrfModelManager()

    history = HistoricalRecords()

    def common_clean(self):
        if self.circumcised == 'Yes' and not self.health_benefits_smc:
            raise CircumcisionError('if \'YES\', what are the benefits of male circumcision?.')
        if self.when_circ and not self.age_unit_circ:
            raise CircumcisionError('If you answered age of circumcision then you must provide time units.')
        if not self.when_circ and self.age_unit_circ:
            raise CircumcisionError(
                'If you did not answer age of circumcision then you must not provide time units.')
        super().common_clean()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = "Circumcision"
        verbose_name_plural = "Circumcision"
