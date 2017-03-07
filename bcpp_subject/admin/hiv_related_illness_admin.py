from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..models import HivRelatedIllness
from ..forms import HivRelatedIllnessForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(HivRelatedIllness, site=bcpp_subject_admin)
class HivRelatedIllnessAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = HivRelatedIllnessForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_visit',
                'sti_dx',
                'sti_dx_other',
                'wasting_date',
                'diarrhoea_date',
                'yeast_infection_date',
                'pneumonia_date',
                'pcp_date',
                'herpes_date',
                'comments',)}),
        audit_fieldset_tuple,
    )

    filter_horizontal = ('sti_dx',)
