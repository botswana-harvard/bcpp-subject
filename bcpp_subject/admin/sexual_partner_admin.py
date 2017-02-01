from django.contrib import admin
from django.utils.translation import ugettext as _

from edc_base.fieldsets import Remove
from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..constants import T0, T1, T2, T3, E0
from ..forms import RecentPartnerForm, SecondPartnerForm, ThirdPartnerForm
from ..models import RecentPartner, SecondPartner, ThirdPartner

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(RecentPartner, site=bcpp_subject_admin)
class RecentPartnerAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = RecentPartnerForm

    conditional_fieldlist = {
        T0: Remove(['first_exchange2', 'first_exchange2_age_other']),
        T1: Remove(['first_exchange']),
        T2: Remove(['first_exchange']),
        T3: Remove(['first_exchange']),
        E0: Remove(['first_exchange']),
    }

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'first_partner_live',
                'sex_partner_community',
                'third_last_sex',
                'third_last_sex_calc',
                'first_first_sex',
                'first_first_sex_calc',
                'first_sex_current',
                'first_relationship',
                'first_exchange',
                'first_exchange2',
                'first_exchange2_age_other',
                'concurrent',
                'goods_exchange',
                'first_sex_freq',
                'first_partner_hiv',
                'partner_hiv_test',
                'first_haart',
                'first_disclose',
                'first_condom_freq',
                'first_partner_cp')}),
        audit_fieldset_tuple,
    )

    # exclude = ('first_partner_arm', 'report_datetime', 'past_year_sex_freq')

    radio_fields = {
        'third_last_sex': admin.VERTICAL,
        'first_first_sex': admin.VERTICAL,
        'first_sex_current': admin.VERTICAL,
        'first_relationship': admin.VERTICAL,
        'concurrent': admin.VERTICAL,
        'sex_partner_community': admin.VERTICAL,
        'past_year_sex_freq': admin.VERTICAL,
        'goods_exchange': admin.VERTICAL,
        'first_exchange': admin.VERTICAL,
        'first_exchange2': admin.VERTICAL,
        'first_partner_hiv': admin.VERTICAL,
        'partner_hiv_test': admin.VERTICAL,
        'first_haart': admin.VERTICAL,
        'first_disclose': admin.VERTICAL,
        'first_condom_freq': admin.VERTICAL,
        'first_partner_cp': admin.VERTICAL, }

    filter_horizontal = ('first_partner_live',)

    instructions = [(
        'Interviewer Note: Ask the respondent to answer'
        ' the following questions about their most recent'
        ' sexual partner in the past 12 months. It may be'
        ' helpful for respondent to give initials or'
        ' nickname, but DO NOT write down or otherwise'
        'record this information. '),
        _('Read to Participant: I am now going to ask you'
          ' about your most recent sexual partners. I will'
          ' start with your last or most recent sexual partner.')]


@admin.register(SecondPartner, site=bcpp_subject_admin)
class SecondPartnerAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = SecondPartnerForm

    conditional_fieldlist = {
        T0: Remove(['first_exchange2', 'first_exchange2_age_other']),
        T1: Remove(['first_exchange']),
        T2: Remove(['first_exchange']),
        T3: Remove(['first_exchange']),
        E0: Remove(['first_exchange']),
    }

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'first_partner_live',
                'sex_partner_community',
                'third_last_sex',
                'third_last_sex_calc',
                'first_first_sex',
                'first_first_sex_calc',
                'first_sex_current',
                'first_relationship',
                'first_exchange',
                'first_exchange2',
                'first_exchange2_age_other',
                'concurrent',
                'goods_exchange',
                'first_sex_freq',
                'first_partner_hiv',
                'partner_hiv_test',
                'first_haart',
                'first_disclose',
                'first_condom_freq',
                'first_partner_cp',)}),
        audit_fieldset_tuple,
    )

    # exclude = ('second_partner_arm', 'report_datetime', 'past_year_sex_freq')

    radio_fields = {
        'third_last_sex': admin.VERTICAL,
        'first_first_sex': admin.VERTICAL,
        'first_sex_current': admin.VERTICAL,
        'first_relationship': admin.VERTICAL,
        'concurrent': admin.VERTICAL,
        'goods_exchange': admin.VERTICAL,
        'sex_partner_community': admin.VERTICAL,
        'past_year_sex_freq': admin.VERTICAL,
        'first_exchange': admin.VERTICAL,
        'first_exchange2': admin.VERTICAL,
        'first_partner_hiv': admin.VERTICAL,
        'partner_hiv_test': admin.VERTICAL,
        'first_haart': admin.VERTICAL,
        'first_disclose': admin.VERTICAL,
        'first_condom_freq': admin.VERTICAL,
        'first_partner_cp': admin.VERTICAL, }

    filter_horizontal = ('first_partner_live',)

    instructions = [(
        'Interviewer Note: If the respondent has only had '
        ' one partner, SKIP to HIV adherence questions if HIV'
        ' negative. Else go to Reproductive health for women,'
        ' or circumcision for men. Ask the respondent to'
        ' answer the following questions about their second'
        ' most recent sexual partner. It may be helpful for'
        ' respondent to give initials or nickname, but DO NOT'
        ' write down or otherwise record this information.'),
        _('Read to Participant: I am now going to ask you about'
          ' your second most recent sexual partner in the past,'
          'the one before the person we were just talking about.')]


@admin.register(ThirdPartner, site=bcpp_subject_admin)
class ThirdPartnerAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = ThirdPartnerForm

    conditional_fieldlist = {
        T0: Remove(['first_exchange2', 'first_exchange2_age_other']),
        T1: Remove(['first_exchange']),
        T2: Remove(['first_exchange']),
        T3: Remove(['first_exchange']),
        E0: Remove(['first_exchange']),
    }

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'first_partner_live',
                'sex_partner_community',
                'third_last_sex',
                'third_last_sex_calc',
                'first_first_sex',
                'first_first_sex_calc',
                'first_sex_current',
                'first_relationship',
                'first_exchange',
                'first_exchange2',
                'first_exchange2_age_other',
                'concurrent',
                'goods_exchange',
                'first_sex_freq',
                'first_partner_hiv',
                'partner_hiv_test',
                'first_haart',
                'first_disclose',
                'first_condom_freq',
                'first_partner_cp',)}),
        audit_fieldset_tuple,
    )

    # exclude = ('third_partner_arm', 'report_datetime', 'past_year_sex_freq')

    radio_fields = {
        'third_last_sex': admin.VERTICAL,
        'first_first_sex': admin.VERTICAL,
        'first_sex_current': admin.VERTICAL,
        'first_relationship': admin.VERTICAL,
        'concurrent': admin.VERTICAL,
        'goods_exchange': admin.VERTICAL,
        'sex_partner_community': admin.VERTICAL,
        'past_year_sex_freq': admin.VERTICAL,
        'first_exchange': admin.VERTICAL,
        'first_exchange2': admin.VERTICAL,
        'first_partner_hiv': admin.VERTICAL,
        'partner_hiv_test': admin.VERTICAL,
        'first_haart': admin.VERTICAL,
        'first_disclose': admin.VERTICAL,
        'first_condom_freq': admin.VERTICAL,
        'first_partner_cp': admin.VERTICAL, }

    filter_horizontal = ('first_partner_live',)

    instructions = [(
        'Interviewer Note: If the respondent has only had '
        ' two partners, SKIP HIV adherence questions if HIV'
        ' negative, if HIV positive, proceed. Else go to '
        'Reproductive health for women,'
        ' or circumcision for men. Ask the respondent to'
        ' answer the following questions about their second'
        ' most recent sexual partner. It may be helpful for'
        ' respondent to give initials or nickname, but DO NOT'
        ' write down or otherwise record this information.'
    ),
        _('Read to Participant: I am now going to ask you about'
          'your second most recent sexual partner in the past'
          ' 12 months, the one before the person we were just'
          'talking about.')]
