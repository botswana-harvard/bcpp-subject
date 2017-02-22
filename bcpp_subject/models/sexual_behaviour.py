from django.core.validators import MinValueValidator, MaxValueValidator,\
    RegexValidator
from django.db import models

from edc_base.model.models import HistoricalRecords
from edc_constants.choices import YES_NO_DWTA

from ..choices import ALCOHOL_SEX, PARTNER_AGE
from .model_mixins import CrfModelMixin, CrfModelManager
from django.utils.safestring import mark_safe
from edc_constants.constants import NOT_APPLICABLE


class SexualBehaviour (CrfModelMixin):

    """A model completed by the user on the participant's sexual behaviour.
    """

    ever_sex = models.CharField(
        verbose_name=mark_safe(
            'In your lifetime, have you ever had sex with anyone? '
            '<span style="font-weight:normal;">(including your spouse, '
            'friends, or someone you have just met.)</span>'),
        max_length=25,
        choices=YES_NO_DWTA,
        help_text='')

    lifetime_sex_partners = models.CharField(
        max_length=10,
        verbose_name='In your lifetime, how many different people have you had '
                     'sex with?',
        validators=[RegexValidator(
            r'^([1-9][0-9]*)|([0])$', 'Expected a number greater than or equal to zero')],
        null=True,
        blank=True,
        help_text=mark_safe(
            '<p><i>Please remember to include casual and once-off partners</br>'
            '(prostitutes and truck drivers) as well as long-term partners</br>'
            '(spouses, boyfriends/girlfriends).<br>'
            'If you can\'t recall the exact number, please give a best guess.</i></p>'),
    )

    last_year_partners = models.CharField(
        max_length=10,
        verbose_name='In the past 12 months, how many different people have you had '
                     'sex with?',
        validators=[RegexValidator(
            r'^([1-9][0-9]*)|([0])$', 'Expected a number greater than or equal to zero')],
        null=True,
        blank=True,
        help_text=mark_safe(
            '<p><i>Please remember to include casual and once-off partners</br>'
            '(prostitutes and truck drivers) as well as long-term partners</br>'
            '(spouses, boyfriends/girlfriends).<br>'
            'If you can\'t recall the exact number, please give a best guess.</i></br>'
            'Leave blank if participant does not want to respond.</p>'),
    )

    more_sex = models.CharField(
        verbose_name='In the past 12 months, did you have sex with somebody '
                     'living outside of the community?',
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text='',
    )

    first_sex = models.IntegerField(
        verbose_name=(
            'How old were you when you had sex for the first time? '
            'If you can\'t recall the exact age, please give a best guess.'),
        null=True,
        blank=True,
        validators=[MinValueValidator(10), MaxValueValidator(64)],
        help_text='Note:leave blank if participant does not want to respond.')

    first_sex_partner_age = models.CharField(
        verbose_name=(
            'How old was your sex partner when you had sex for the first time'),
        max_length=25,
        choices=PARTNER_AGE,
        default=NOT_APPLICABLE,
    )

    first_sex_partner_age_other = models.IntegerField(
        verbose_name='If 19 or older, specify age',
        null=True,
        blank=True,
    )

    condom = models.CharField(
        verbose_name='During the last most recent time you had sex, did '
                     'you or your partner use a condom?',
        max_length=25,
        null=True,
        blank=True,
        choices=YES_NO_DWTA,
        help_text='',
    )

    alcohol_sex = models.CharField(
        verbose_name='During the last most recent time you had sex, were'
                     ' you or your partner drinking alcohol?',
        max_length=25,
        null=True,
        blank=True,
        choices=ALCOHOL_SEX,
        help_text='',
    )

    objects = CrfModelManager()

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'bcpp_subject'
        verbose_name = 'Sexual Behaviour'
        verbose_name_plural = 'Sexual Behaviour'
