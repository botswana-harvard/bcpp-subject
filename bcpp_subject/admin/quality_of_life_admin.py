from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import QualityOfLifeForm
from ..models import QualityOfLife
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(QualityOfLife, site=bcpp_subject_admin)
class QualityOfLifeAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = QualityOfLifeForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'mobility',
                'self_care',
                'activities',
                'pain',
                'anxiety',
                'health_today')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'mobility': admin.VERTICAL,
        'self_care': admin.VERTICAL,
        'activities': admin.VERTICAL,
        'pain': admin.VERTICAL,
        'anxiety': admin.VERTICAL,
    }

    additional_instructions = mark_safe(
        '<h5>Note to Interviewer</h5>'
        'In this section, read the heading '
        '(question) and then each of the 5 possible responses for each '
        'question. Do not read -Do not want to answer-, but record '
        'this if respondent declines to answer.'
        '<H5><span style="color:orange;">Read to Participant</span></H5>'
        'To start, I will ask some questions '
        'regarding your overall health. Under each heading, please indicate '
        'the ONE statement that best describes your health TODAY.')
