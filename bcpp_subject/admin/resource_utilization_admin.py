from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import ResourceUtilizationForm
from ..models import ResourceUtilization
from .modeladmin_mixins import CrfModelAdminMixin
from django.utils.safestring import mark_safe


@admin.register(ResourceUtilization, site=bcpp_subject_admin)
class ResourceUtilizationAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = ResourceUtilizationForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'out_patient',
                'hospitalized',
                'money_spent',
                'medical_cover')}),
        audit_fieldset_tuple
    )

    radio_fields = {
        'out_patient': admin.VERTICAL,
        'medical_cover': admin.VERTICAL,
    }

    additional_instructions = mark_safe(
        '<h5>Note to Interviewer</h5> Complete this interview with the '
        'participant and enter the participant\'s response for each question. '
        'Each question is to be answered by the participant, not the '
        'interviewer. Please check only one box for each question.'
        '<H5><span style="color:orange;">Read to Participant</span></H5>'
        'Next, I will ask questions about health '
        'care visits over the past three months. Please think about all '
        'visits for any health issue, including pregnancy.')
