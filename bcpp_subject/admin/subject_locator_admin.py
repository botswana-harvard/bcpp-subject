from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_base.fieldsets import Remove

from ..admin_site import bcpp_subject_admin
from ..forms import SubjectLocatorForm
from ..models import SubjectLocator
from ..constants import E0
from .modeladmin_mixins import ModelAdminMixin


@admin.register(SubjectLocator, site=bcpp_subject_admin)
class SubjectLocatorAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = SubjectLocatorForm

    conditional_fieldlists = {
        E0: Remove('mail_address'),
    }

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'date_signed',
                'mail_address',
                'home_visit_permission',
                'physical_address',
                'may_follow_up',
                'subject_cell',
                'subject_cell_alt',
                'subject_phone',
                'subject_phone_alt')}),
        audit_fieldset_tuple,
    )

    radio_fields = {
        'home_visit_permission': admin.VERTICAL,
        'may_follow_up': admin.VERTICAL,
        'has_alt_contact': admin.VERTICAL,
        'may_call_work': admin.VERTICAL,
        'may_contact_someone': admin.VERTICAL, }

    list_filter = (
        'may_follow_up',
        'may_contact_someone',
        'may_call_work',
        'home_visit_permission')

    list_display = (
        'subject_identifier',
        'date_signed',
        'home_visit_permission',
        'may_follow_up',
        'has_alt_contact',
        'may_call_work',
        'may_contact_someone')
