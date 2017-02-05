from django.contrib import admin
from django.utils.safestring import mark_safe

from ..admin_site import bcpp_subject_admin
from ..forms import RecentPartnerForm
from ..models import RecentPartner
from .modeladmin_mixins import CrfModelAdminMixin, SexualPartnerAdminMixin


@admin.register(RecentPartner, site=bcpp_subject_admin)
class RecentPartnerAdmin(SexualPartnerAdminMixin, CrfModelAdminMixin, admin.ModelAdmin):

    form = RecentPartnerForm

    additional_instructions = mark_safe(
        '<H5>Interviewer Note</H5> Ask the respondent to answer'
        'the following questions about their most recent '
        'sexual partner in the past 12 months. It may be '
        'helpful for respondent to give initials or '
        'nickname, but DO NOT write down or otherwise '
        'record this information. '
        '<H5><span style=\"color:orange;\">Read to Participant</span></H5>'
        'I am now going to ask you about your most recent sexual partners. '
        'I will start with your <b>last or most recent</b> sexual partner that '
        'you had within the last 12 months')
