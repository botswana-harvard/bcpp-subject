from django.db import models

from edc_constants.choices import (
    YES_NO_DWTA, YES_NO_UNSURE_DWTA, YES_NO_UNSURE)
from edc_constants.constants import OTHER, NOT_APPLICABLE
from edc_map.site_mappers import site_mappers

from ...choices import (
    COMMUNITY_NA, FREQ_IN_YEAR, SEXDAYS_CHOICE, LASTSEX_CHOICE,
    FIRSTRELATIONSHIP_CHOICE, AGE_RANGES, FIRST_DISCLOSE_CHOICE,
    FIRST_CONDOM_FREQ_CHOICE, FIRST_PARTNER_HIV_CHOICE)
from ...constants import CPC, ECC
from ..list_models import PartnerResidency
from bcpp_subject.choices import PARTNER_AGE


class SexualPartnerMixin (models.Model):

    first_partner_live = models.ManyToManyField(
        PartnerResidency,
        verbose_name="Over the past 12 months, where has this sexual partner"
                     " lived to the best of your knowledge?",
        help_text="")

    sex_partner_community = models.CharField(
        verbose_name=(
            'If outside community or farm outside this community or cattle post '
            'outside this community ask: Does this sexual partner live in any '
            'of the following communities?'),
        max_length=25,
        choices=COMMUNITY_NA,
        help_text="")

    past_year_sex_freq = models.CharField(
        verbose_name=(
            'Approximately how often did you have sex with this partner '
            'during the past 12 months?'),
        max_length=25,
        choices=FREQ_IN_YEAR,
        help_text="")

    third_last_sex = models.CharField(
        verbose_name="When was the last [most recent] time you had sex with"
                     " this person (how long ago)?",
        max_length=25,
        choices=SEXDAYS_CHOICE,
        help_text="")

    third_last_sex_calc = models.IntegerField(
        verbose_name=(
            'Give the number of days/months since last had sex with this person.'),
        null=True,
        blank=True,
        help_text=(
            'e.g. if last sex was last night, then it should be recorded as 1 day'))

    first_first_sex = models.CharField(
        verbose_name=(
            'When was the first time you had sex with this person [how long ago]?'),
        max_length=25,
        choices=LASTSEX_CHOICE,
        help_text="")

    first_first_sex_calc = models.IntegerField(
        verbose_name=(
            'Give the number of days/months/years since first had sex with '
            'this person.'),
        null=True,
        blank=True,
        help_text=('e.g. if first sex was last night, then it should be '
                   'recorded as 1 day'))

    first_sex_current = models.CharField(
        verbose_name="Do you expect to have sex with this person again?",
        max_length=25,
        choices=YES_NO_DWTA,
        help_text="")

    first_relationship = models.CharField(
        verbose_name="What type of relationship do you have with this person?",
        max_length=40,
        choices=FIRSTRELATIONSHIP_CHOICE,
        help_text="")

    first_exchange = models.CharField(
        verbose_name="To the best of your knowledge, how old is this person?",
        max_length=40,
        choices=AGE_RANGES,
        null=True,
        blank=False,
        help_text=("Note: If participant does not want to answer, leave blank."))

    first_exchange2 = models.CharField(
        max_length=25,
        choices=PARTNER_AGE,
        null=True,
        blank=False,
    )

    # FIXME: add validation in form
    first_exchange2_age_other = models.IntegerField(
        verbose_name='If 19 or older, specify age',
        null=True,
        blank=True,
    )

    concurrent = models.CharField(
        verbose_name=(
            'Over the past 12 months, during the time you were having a sexual '
            'relationship with this person, did YOU have sex with other people '
            ' (including husband/wife)?'),
        max_length=25,
        choices=YES_NO_DWTA,
        help_text="")

    goods_exchange = models.CharField(
        verbose_name=(
            'Have you received money, transport, food/drink, or other goods '
            'in exchange for sex from this partner?'),
        max_length=25,
        choices=YES_NO_DWTA,
        help_text="")

    first_sex_freq = models.IntegerField(
        verbose_name=(
            'During the last 3 months [of your relationship, if it has ended] '
            'how many times did you have sex with this partner?'),
        null=True,
        blank=True,
        help_text="")

    first_partner_hiv = models.CharField(
        verbose_name="What is this partner's HIV status?",
        max_length=25,
        choices=FIRST_PARTNER_HIV_CHOICE,
        null=True,
        help_text="")

    partner_hiv_test = models.CharField(
        verbose_name="Has your partner been tested for HIV in last 12 months",
        choices=YES_NO_UNSURE_DWTA,
        max_length=25,
        help_text="")

    first_haart = models.CharField(
        verbose_name="Is this partner taking antiretroviral treatment?",
        max_length=25,
        choices=YES_NO_UNSURE,
        null=True,
        blank=True,
        help_text="")

    first_disclose = models.CharField(
        verbose_name="Have you told this partner your HIV status?",
        max_length=30,
        choices=FIRST_DISCLOSE_CHOICE,
        null=True,
        help_text="")

    first_condom_freq = models.CharField(
        verbose_name="When you have [had] sex with this partner, how often "
                     "do you or your partner use a condom?",
        max_length=25,
        choices=FIRST_CONDOM_FREQ_CHOICE,
        null=True,
        help_text="")

    first_partner_cp = models.CharField(
        verbose_name=(
            'To the best of your knowledge, did he/she ever have '
            'other sex partners while you two were having a sexual relationship?'),
        max_length=25,
        choices=YES_NO_UNSURE,
        null=True,
        help_text="")

    def skip_logic_questions(self, first_partner_choices):
        # FIXME: yuk
        first_partner_choices = first_partner_choices or []
        first_partner_live = [
            'In this community',
            'Farm within this community', 'Cattle post within this community']
        skip = False
        not_skip = False
        in_out_comm = []
        for partner in first_partner_choices:
            if partner.name in first_partner_live:
                skip = True
            if 'In this community' == partner.name:
                in_out_comm.append(partner.name)
            if 'Outside community' == partner.name:
                in_out_comm.append(partner.name)
            if len(in_out_comm) == 2:
                return not_skip
        return skip and not not_skip

    def is_ecc_or_cpc(self):
        # TODO: how better to determine is intervention?
        if self.sex_partner_community not in [NOT_APPLICABLE, OTHER, None]:
            if site_mappers.registry.get(
                    self.sex_partner_community.lower()).intervention:
                return CPC
            else:
                return ECC
        return False

    def get_partner_arm(self):
        if self.is_ecc_or_cpc():
            partner_arm = self.is_ecc_or_cpc()
        elif self.sex_partner_community == NOT_APPLICABLE:
            partner_arm = NOT_APPLICABLE
        elif self.sex_partner_community == OTHER:
            partner_arm = OTHER
        else:
            partner_arm = ''
        return partner_arm

    class Meta:
        abstract = True
