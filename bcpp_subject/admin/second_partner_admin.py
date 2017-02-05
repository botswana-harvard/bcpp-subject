from django.contrib import admin
from django.utils.safestring import mark_safe

from ..admin_site import bcpp_subject_admin
from ..forms import SecondPartnerForm
from ..models import SecondPartner
from .modeladmin_mixins import CrfModelAdminMixin, SexualPartnerAdminMixin


@admin.register(SecondPartner, site=bcpp_subject_admin)
class SecondPartnerAdmin(SexualPartnerAdminMixin, CrfModelAdminMixin, admin.ModelAdmin):

    form = SecondPartnerForm

    additional_instructions = mark_safe(
        '<H5>Interviewer Note</H5> If the respondent has only had '
        'one partner, SKIP to HIV adherence questions if HIV '
        'negative. Else go to Reproductive health for women, '
        'or circumcision for men. Ask the respondent to '
        'answer the following questions about their second '
        'most recent sexual partner. It may be helpful for '
        'respondent to give initials or nickname, but DO NOT '
        'write down or otherwise record this information. '
        '<H5><span style=\"color:orange;\">Read to Participant</span></H5>'
        'I am now going to ask you about '
        'your <b>second</b> most recent sexual partner in the past, '
        'the one before the person we were just talking about.')
