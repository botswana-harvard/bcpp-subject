from django.contrib import admin

from ..admin_site import bcpp_subject_admin
from ..models import Sti
from ..forms import StiForm

from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(Sti, site=bcpp_subject_admin)
class StiAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = StiForm
    fields = (
        'subject_visit',
        'sti_dx',
        'sti_dx_other',
        'wasting_date',
        'diarrhoea_date',
        'yeast_infection_date',
        'pneumonia_date',
        'pcp_date',
        'herpes_date',
        'comments',)
    filter_horizontal = ('sti_dx',)
