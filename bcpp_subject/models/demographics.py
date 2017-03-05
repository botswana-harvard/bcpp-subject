from django.db import models

from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords


from ..choices import MARITAL_STATUS_CHOICE, RELIGION, ETHNIC_GROUP

from .list_models import LiveWith
from .model_mixins import CrfModelMixin, CrfModelManager


class Demographics (CrfModelMixin):

    """A model completed by the user of the basic demographics
    of the participant.
    """

    religion = models.CharField(
        verbose_name='What is your religious affiliation?',
        max_length=25,
        choices=RELIGION,
        null=True,
        blank=False)

    religion_other = OtherCharField()

    ethnic = models.CharField(
        verbose_name='What is your ethnic group?',
        max_length=25,
        choices=ETHNIC_GROUP,
        null=True,
        blank=False,
        help_text='Ask for the original ethnic group')

    ethnic_other = OtherCharField()

    marital_status = models.CharField(
        verbose_name='What is your current marital status?',
        max_length=55,
        choices=MARITAL_STATUS_CHOICE,
        help_text='')

    num_wives = models.IntegerField(
        verbose_name=(
            'WOMEN: How many wives does your husband have '
            '(including traditional marriage),'
            ' including yourself?'),
        null=True,
        blank=True,
        help_text=('Leave blank if participant does not '
                   'want to respond. (women only)'))

    husband_wives = models.IntegerField(
        verbose_name=('MEN: How many wives do you have, '
                      'including traditional marriage?'),
        null=True,
        blank=True,
        help_text=('Leave blank if participant does not '
                   'want to respond. (men only)'))

    live_with = models.ManyToManyField(
        LiveWith,
        verbose_name='Who do you currently live with?')

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = 'Demographics'
        verbose_name_plural = 'Demographics'
