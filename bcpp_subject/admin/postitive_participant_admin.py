from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import PositiveParticipantForm
from ..models import PositiveParticipant
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(PositiveParticipant, site=bcpp_subject_admin)
class PositiveParticipantAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = PositiveParticipantForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'internalize_stigma',
                'internalized_stigma',
                'friend_stigma',
                'family_stigma',
                'enacted_talk_stigma',
                'enacted_respect_stigma',
                'enacted_jobs_tigma')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'internalize_stigma': admin.VERTICAL,
        'internalized_stigma': admin.VERTICAL,
        'friend_stigma': admin.VERTICAL,
        'family_stigma': admin.VERTICAL,
        'enacted_talk_stigma': admin.VERTICAL,
        'enacted_respect_stigma': admin.VERTICAL,
        'enacted_jobs_tigma': admin.VERTICAL, }

    additional_instructions = mark_safe(
        '<h5>Note to Interviewer</h5>'
        'Note The following supplemental questions '
        'are only asked for respondents with known HIV infection. '
        'SKIP for respondents without known HIV infection. '
        '<H5><span style="color:orange;">Read to Participant</span></H5>'
        'You let us know earlier that you '
        'are HIV positive. I would now like to ask you a few '
        'questions about your experiences living with HIV. '
        'Please remember this interview and your responses '
        'are private and confidential.In this section, '
        'I\'m going to read you statements '
        'about how you may feel about yourself and your '
        'HIV/AIDS infection. I would like you to tell me '
        'if you strongly agree, agree, disagree or strongly '
        'disagree with each statement?')
