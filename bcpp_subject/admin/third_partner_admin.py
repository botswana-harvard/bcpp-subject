from django.contrib import admin
from django.utils.safestring import mark_safe

from ..admin_site import bcpp_subject_admin
from ..forms import ThirdPartnerForm
from ..models import ThirdPartner
from .modeladmin_mixins import CrfModelAdminMixin, SexualPartnerAdminMixin


@admin.register(ThirdPartner, site=bcpp_subject_admin)
class ThirdPartnerAdmin(SexualPartnerAdminMixin, CrfModelAdminMixin, admin.ModelAdmin):

    form = ThirdPartnerForm

    additional_instructions = mark_safe(
        'Interviewer Note: If the respondent has only had '
        'two partners, SKIP HIV adherence questions if HIV '
        'negative, if HIV positive, proceed. Else go to '
        'Reproductive health for women, '
        'or circumcision for men. Ask the respondent to '
        'answer the following questions about their second '
        'most recent sexual partner. It may be helpful for '
        'respondent to give initials or nickname, but DO NOT '
        'write down or otherwise record this information. '
        '<H5><span style=\"color:orange;\">Read to Participant</span></H5>'
        'I am now going to ask you about '
        'your <b>third</b> most recent sexual partner in the past '
        '12 months, the one before the person we were just '
        'talking about.')
