from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..models import HeartAttack
from ..forms import HeartAttackForm

from .modeladmin_mixins import CrfModelAdminMixin
from django.utils.safestring import mark_safe


@admin.register(HeartAttack, site=bcpp_subject_admin)
class HeartAttackAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HeartAttackForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'heart_attack_date',
                'heart_attack_dx',
                'heart_attack_dx_other',)}),
        audit_fieldset_tuple
    )

    filter_horizontal = ('dx_heart_attack',)

    additional_instructions = mark_safe(
        '<H5>Note to Interviewer</H5>This form is to be filled '
        'for all participants even if they do not have a record '
        '(on hand) of the diagnosis.')
