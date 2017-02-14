from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_base.fieldsets import Remove
from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..constants import T0, E0
from ..forms import ReproductiveHealthForm
from ..models import ReproductiveHealth
from .modeladmin_mixins import CrfModelAdminMixin

fields = (
    'when_pregnant',
    'gestational_weeks',
    'pregnancy_hiv_tested',
    'pregnancy_hiv_retested')


@admin.register(ReproductiveHealth, site=bcpp_subject_admin)
class ReproductiveHealthAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = ReproductiveHealthForm

    custom_form_labels = {
        'given_birth': {
            'label': 'Have you given birth since we last spoke in {previous}',
            'callback': lambda obj: True if obj else False},
        'menopause': {
            'label': (
                'Have you reached menopause (more than 12 months without a period) '
                'since we last spoke in {previous}?'),
            'callback': lambda obj: True if obj else False}
    }

    conditional_fieldlists = {
        T0: Remove(
            'when_pregnant', 'gestational_weeks', 'pregnancy_hiv_tested',
            'pregnancy_hiv_retested', 'given_birth', 'more_children'),
        E0: Remove('given_birth', 'more_children'),
    }

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'number_children',
                'given_birth',
                'menopause',
                'more_children',
                'family_planning',
                'family_planning_other',
                'currently_pregnant',
                'when_pregnant',
                'gestational_weeks',
                'pregnancy_hiv_tested',
                'pregnancy_hiv_retested')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'given_birth': admin.VERTICAL,
        'menopause': admin.VERTICAL,
        'more_children': admin.VERTICAL,
        'currently_pregnant': admin.VERTICAL,
        'when_pregnant': admin.VERTICAL,
        'pregnancy_hiv_tested': admin.VERTICAL,
        'pregnancy_hiv_retested': admin.VERTICAL
    }

    filter_horizontal = ('family_planning',)

    additional_instructions = mark_safe(
        '<h5>Note to Interviewer</h5> This section is to be'
        'completed by female participants. SKIP for male participants.'
        '<H5><span style="color:orange;">Read to Participant</span></H5>'
        'I am now going to ask you questions '
        'about reproductive health and pregnancy')
