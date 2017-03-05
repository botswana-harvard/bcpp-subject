from django.contrib import admin

from edc_base.modeladmin_mixins import audit_fieldset_tuple

from ..admin_site import bcpp_subject_admin
from ..forms import SubjectLocatorForm
from ..models import SubjectLocator
from .modeladmin_mixins import ModelAdminMixin, FieldsetsModelAdminMixin
from ..models.subject_visit import SubjectVisit
from ..constants import E0


@admin.register(SubjectLocator, site=bcpp_subject_admin)
class SubjectLocatorAdmin(ModelAdminMixin, FieldsetsModelAdminMixin,
                          admin.ModelAdmin):

    form = SubjectLocatorForm

    def get_fieldsets(self, request, obj=None):
        """Returns fieldsets after modifications declared in
        "conditional" dictionaries.
        """
        fieldsets = super().get_fieldsets(request, obj=obj)
        subject_identifier = request.GET.get('subject_identifier')
        try:
            subject_visit = SubjectVisit.objects.get(subject_identifier=subject_identifier)
            if subject_visit.visit_code == E0:
                fields = fieldsets[0][1].get('fields')
                field_list = []
                for field in fields:
                    field_list.append(field)
                field_list.remove('mail_address')
                fields = ()
                for field in field_list:
                    fields += (field,)
                fieldsets[0][1].update(fields=fields)
        except SubjectVisit.DoesNotExist:
            pass
        except SubjectVisit.MultipleObjectsReturned:
            pass
        return fieldsets

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
