from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import StigmaOpinionForm
from ..models import StigmaOpinion

from .modeladmin_mixins import CrfModelAdminMixin
from django.utils.safestring import mark_safe


@admin.register(StigmaOpinion, site=bcpp_subject_admin)
class StigmaOpinionAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = StigmaOpinionForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'test_community_stigma',
                'gossip_community_stigma',
                'respect_community_stigma',
                'enacted_verbal_stigma',
                'enacted_physical_stigma',
                'enacted_family_stigma',
                'fear_stigma')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'test_community_stigma': admin.VERTICAL,
        'gossip_community_stigma': admin.VERTICAL,
        'respect_community_stigma': admin.VERTICAL,
        'enacted_verbal_stigma': admin.VERTICAL,
        'enacted_physical_stigma': admin.VERTICAL,
        'enacted_family_stigma': admin.VERTICAL,
        'fear_stigma': admin.VERTICAL, }

    additional_instructions = mark_safe(
        '<H5><span style=\"color:orange;\">Read to Participant</span></H5>'
        'Using your own opinions and '
        'thinking about this community, please tell me how '
        'strongly you agree or disagree with the following '
        'statements.')
