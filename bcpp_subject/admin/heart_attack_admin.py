from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..models import HeartAttack
from ..forms import HeartAttackForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HeartAttack, site=bcpp_subject_admin)
class HeartAttackAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HeartAttackForm
    fields = (
        'subject_visit',
        'date_heart_attack',
        'dx_heart_attack',
        'dx_heart_attack_other',)
    filter_horizontal = ('dx_heart_attack',)
    instructions = [(
        'Note to Interviewer: This form is to be filled for all participants'
        ' even if they do not have a record (on hand) of the diagnosis.')]
